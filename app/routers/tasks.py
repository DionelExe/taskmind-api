"""Endpoints HTTP para tareas."""

from typing import Any

from fastapi import APIRouter


router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.get("/")
async def get_tasks() -> dict[str, Any]:
    """Endpoint de prueba para consultar tareas."""
    return {"message": "Tasks endpoint is ready", "tasks": []}


@router.post("/")
async def create_task(task: dict[str, Any]) -> dict[str, Any]:
    """Crea una tarea de ejemplo, preparada para priorización con Gemini."""
    return {
        "message": "Task endpoint is ready for Gemini prioritization",
        "task": task,
        "priority": None,
    }
