"""Pruebas del microservicio de notificaciones."""

import pytest
from httpx import ASGITransport, AsyncClient

from notification_service.main import app


@pytest.mark.asyncio
async def test_notification_service_health() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Notification Service is running"}


@pytest.mark.asyncio
async def test_notification_service_accepts_notification() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/notifications",
            json={
                "recipient": "test-user",
                "title": "Task created",
                "message": "A task was created",
            },
        )

    assert response.status_code == 202
    assert response.json()["status"] == "accepted"
