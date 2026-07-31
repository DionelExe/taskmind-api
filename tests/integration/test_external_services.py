"""Pruebas de integración opcionales contra Firebase y Gemini reales."""

import asyncio
import os
from pathlib import Path

import pytest

from app.routers.tasks import classify_priority


def _integration_credentials_available() -> bool:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    return bool(
        os.getenv("GEMINI_API_KEY")
        and credentials_path
        and Path(credentials_path).is_file()
        and Path(credentials_path).stat().st_size > 0
    )


pytestmark = pytest.mark.skipif(
    not _integration_credentials_available(),
    reason="Faltan GEMINI_API_KEY o credenciales de Firebase.",
)


@pytest.mark.asyncio
async def test_gemini_classifies_a_task() -> None:
    priority = await classify_priority(
        "Prueba de integración",
        "Validar la conexión real con Gemini.",
    )

    assert priority in {"low", "medium", "high"}


@pytest.mark.asyncio
async def test_firestore_connection_is_available() -> None:
    from app.database.firebase import get_firestore_client

    client = await asyncio.to_thread(get_firestore_client)
    documents = await asyncio.to_thread(
        lambda: list(client.collection("tasks").limit(1).stream())
    )

    assert isinstance(documents, list)
