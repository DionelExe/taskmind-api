"""Punto de entrada de TaskMind-API."""

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers.tasks import router as tasks_router


load_dotenv()

app = FastAPI(title="TaskMind-API", version="0.1.0")
app.include_router(tasks_router)


@app.get("/")
async def health_check() -> dict[str, str]:
    """Comprueba que la API está disponible."""
    return {"message": "TaskMind-API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
