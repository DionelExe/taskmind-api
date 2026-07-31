"""Pruebas unitarias de la lógica de tareas."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.routers.tasks import TaskCreate, classify_priority


def test_task_create_requires_title_and_description() -> None:
    task = TaskCreate(title="Comprar leche", description="Antes de volver a casa")

    assert task.title == "Comprar leche"
    assert task.description == "Antes de volver a casa"


@pytest.mark.asyncio
async def test_classify_priority_normalizes_gemini_response() -> None:
    response = Mock(text='{"priority": "HIGH"}')
    client = Mock()
    client.aio.models.generate_content = AsyncMock(return_value=response)

    with patch("app.routers.tasks.genai.Client", return_value=client):
        priority = await classify_priority("Entrega", "Vence hoy")

    assert priority == "high"


@pytest.mark.asyncio
async def test_classify_priority_rejects_invalid_response() -> None:
    response = Mock(text='{"priority": "critical"}')
    client = Mock()
    client.aio.models.generate_content = AsyncMock(return_value=response)

    with patch("app.routers.tasks.genai.Client", return_value=client):
        with pytest.raises(RuntimeError, match="fuera del rango"):
            await classify_priority("Entrega", "Vence hoy")
