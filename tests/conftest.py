"""Fixtures compartidas por las pruebas de TaskMind-API."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.routers.tasks import get_current_user
from main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Crea un cliente HTTP asíncrono contra la aplicación FastAPI."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as test_client:
        yield test_client


@pytest.fixture
def authenticated_user() -> dict[str, str]:
    """Devuelve un usuario de prueba sin contactar Firebase."""
    return {"uid": "test-user-123"}


@pytest.fixture
def override_auth(authenticated_user: dict[str, str]) -> None:
    """Inyecta un usuario autenticado para las pruebas de integración."""
    app.dependency_overrides[get_current_user] = lambda: authenticated_user
    yield
    app.dependency_overrides.clear()
