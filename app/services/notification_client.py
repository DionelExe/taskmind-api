"""Cliente asíncrono para el microservicio de notificaciones."""

import os
from typing import Any

import httpx


async def send_notification(payload: dict[str, Any]) -> dict[str, Any]:
    """Envía una notificación cuando el servicio está configurado."""
    base_url = os.getenv("NOTIFICATION_SERVICE_URL")
    if not base_url:
        return {"status": "disabled"}

    async with httpx.AsyncClient(base_url=base_url, timeout=5.0) as client:
        response = await client.post("/notifications", json=payload)
        response.raise_for_status()
        return response.json()
