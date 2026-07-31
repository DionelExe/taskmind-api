"""Pruebas del endpoint de salud."""

import pytest


@pytest.mark.asyncio
async def test_health_check_returns_running_message(client) -> None:
    response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "TaskMind-API is running"}
