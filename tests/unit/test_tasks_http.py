"""Pruebas unitarias HTTP con dependencias externas simuladas."""

from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock, patch

import pytest


@pytest.mark.asyncio
async def test_create_task_returns_201_and_persists_owner(
    client,
    override_auth,
) -> None:
    document = Mock()
    collection = Mock()
    collection.document.return_value = document
    firestore_client = Mock()
    firestore_client.collection.return_value = collection

    with (
        patch(
            "app.routers.tasks.classify_priority",
            new=AsyncMock(return_value="high"),
        ),
        patch(
            "app.routers.tasks.get_firestore_client",
            return_value=firestore_client,
        ),
    ):
        response = await client.post(
            "/api/v1/tasks/",
            json={
                "title": "Preparar presentación",
                "description": "Terminar las diapositivas para mañana",
            },
        )

    assert response.status_code == 201
    assert response.json()["priority"] == "high"
    assert response.json()["owner_uid"] == "test-user-123"
    document.set.assert_called_once()


@pytest.mark.asyncio
async def test_tasks_requires_authentication(client) -> None:
    response = await client.get("/api/v1/tasks/")

    assert response.status_code == 401
    assert response.json()["detail"] == "Se requiere autenticación."


@pytest.mark.asyncio
async def test_get_tasks_filters_by_authenticated_owner(
    client,
    override_auth,
) -> None:
    document = SimpleNamespace(
        to_dict=lambda: {
            "id": "task-1",
            "owner_uid": "test-user-123",
        }
    )
    query = Mock()
    query.stream.return_value = [document]
    collection = Mock()
    collection.where.return_value = query
    firestore_client = Mock()
    firestore_client.collection.return_value = collection

    with patch(
        "app.routers.tasks.get_firestore_client",
        return_value=firestore_client,
    ):
        response = await client.get("/api/v1/tasks/")

    assert response.status_code == 200
    assert response.json() == {
        "tasks": [{"id": "task-1", "owner_uid": "test-user-123"}]
    }
    collection.where.assert_called_once_with("owner_uid", "==", "test-user-123")
