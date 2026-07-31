"""API independiente para recibir notificaciones de tareas."""

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI(title="TaskMind Notification Service", version="0.1.0")


class NotificationCreate(BaseModel):
    """Datos mínimos de una notificación."""

    recipient: str = Field(min_length=1)
    title: str = Field(min_length=1)
    message: str = Field(min_length=1)


class NotificationResponse(NotificationCreate):
    """Notificación aceptada por el servicio."""

    id: str
    created_at: str
    status: str


@app.get("/")
async def health_check() -> dict[str, str]:
    """Comprueba que el servicio está disponible."""
    return {"message": "Notification Service is running"}


@app.post(
    "/notifications",
    response_model=NotificationResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_notification(
    notification: NotificationCreate,
) -> NotificationResponse:
    """Acepta una notificación para procesamiento posterior."""
    return NotificationResponse(
        **notification.model_dump(),
        id=f"notification-{uuid4().hex}",
        created_at=datetime.now(UTC).isoformat(),
        status="accepted",
    )
