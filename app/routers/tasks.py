"""Endpoints HTTP para tareas."""

import asyncio
import json
import os
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from app.database.firebase import get_firestore_client, initialize_firebase

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])
bearer_scheme = HTTPBearer(auto_error=False)


class TaskCreate(BaseModel):
    """Datos necesarios para crear una tarea."""

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)


class TaskResponse(TaskCreate):
    """Representación persistida de una tarea."""

    id: str
    priority: str
    created_at: str
    owner_uid: str


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict[str, Any]:
    """Valida el Firebase ID token sin bloquear el event loop."""
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere autenticación.",
        )

    try:
        await asyncio.to_thread(initialize_firebase)
        return await asyncio.to_thread(auth.verify_id_token, credentials.credentials)
    except (auth.InvalidIdTokenError, auth.ExpiredIdTokenError, ValueError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token de Firebase no es válido o expiró.",
        ) from error


async def classify_priority(title: str, description: str) -> str:
    """Solicita a Gemini una prioridad normalizada para la tarea."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("La variable GEMINI_API_KEY es obligatoria.")

    client = genai.Client(api_key=api_key)
    prompt = (
        "Clasifica la urgencia de esta tarea como exactamente una de estas opciones: "
        "low, medium o high. Responde únicamente JSON con la clave priority.\n"
        f"Título: {title}\nDescripción: {description}"
    )
    response = await client.aio.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "priority": {
                        "type": "STRING",
                        "enum": ["low", "medium", "high"],
                    }
                },
                "required": ["priority"],
            },
        ),
    )
    try:
        priority = json.loads(response.text)["priority"].lower()
    except (TypeError, json.JSONDecodeError, KeyError, AttributeError) as error:
        raise RuntimeError("Gemini devolvió una prioridad inválida.") from error

    if priority not in {"low", "medium", "high"}:
        raise RuntimeError("Gemini devolvió una prioridad fuera del rango permitido.")
    return priority


@router.get("/")
async def get_tasks(
    user: dict[str, Any] = Depends(get_current_user),
) -> dict[str, list[dict[str, Any]]]:
    """Consulta las tareas del usuario autenticado."""
    client = await asyncio.to_thread(get_firestore_client)
    documents = await asyncio.to_thread(
        lambda: list(
            client.collection("tasks")
            .where("owner_uid", "==", user["uid"])
            .stream()
        )
    )
    return {"tasks": [document.to_dict() for document in documents]}


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate,
    user: dict[str, Any] = Depends(get_current_user),
) -> TaskResponse:
    """Clasifica y persiste una tarea del usuario autenticado."""
    priority = await classify_priority(task.title, task.description)
    created_task = TaskResponse(
        id=uuid4().hex,
        title=task.title,
        description=task.description,
        priority=priority,
        created_at=datetime.now(UTC).isoformat(),
        owner_uid=user["uid"],
    )
    client = await asyncio.to_thread(get_firestore_client)
    await asyncio.to_thread(
        client.collection("tasks").document(created_task.id).set,
        created_task.model_dump(),
    )
    return created_task
