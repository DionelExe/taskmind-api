"""Prueba de carga del endpoint de tareas."""

import os

from locust import HttpUser, between, task


class TaskMindUser(HttpUser):
    """Usuario de carga que crea tareas autenticadas."""

    wait_time = between(1, 3)

    def on_start(self) -> None:
        token = os.getenv("FIREBASE_ID_TOKEN")
        if not token:
            raise RuntimeError("Define FIREBASE_ID_TOKEN para ejecutar Locust.")
        self.client.headers["Authorization"] = "Bearer " + token

    @task
    def create_task(self) -> None:
        response = self.client.post(
            "/api/v1/tasks/",
            json={
                "title": "Prueba de carga",
                "description": "Tarea generada durante la prueba de estrés.",
            },
            name="POST /api/v1/tasks/",
        )
        response.raise_for_status()
