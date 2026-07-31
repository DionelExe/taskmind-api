# TaskMind-API

API FastAPI para gestionar tareas autenticadas con Firebase, clasificar su
prioridad mediante Google GenAI y persistirlas en Firestore.

## Documentación

- [Historias de usuario](docs/user_stories.md)
- [Evidencia TDD](docs/tdd.md)
- [Estrategia de testing](docs/testing.md)
- [Justificación de Cloud Run](docs/cloud-justification.md)
- [Configuración y despliegue](docs/deployment.md)

## Historias de usuario

- Como usuario autenticado, quiero crear una tarea para que Gemini determine
  su prioridad y TaskMind-API la persista en Firestore.
- Como usuario de TaskMind-API, quiero autenticar mis solicitudes con Firebase
  Auth para acceder únicamente a mis tareas.

Los criterios de aceptación de ambas historias están escritos en sintaxis
Gherkin en [docs/user_stories.md](docs/user_stories.md).

## Configuración local

1. Copiá `.env.example` como `.env`.
2. Configurá `GEMINI_API_KEY` y `GOOGLE_APPLICATION_CREDENTIALS`.
3. Guardá la credencial de Firebase fuera del control de versiones como
   `firebase-credentials.json`.
4. Instalá dependencias con `pip install -r requirements-dev.txt`.
5. Ejecutá `uvicorn main:app --reload`.

La documentación interactiva queda disponible en `http://127.0.0.1:8000/docs`.

## Calidad y pruebas

```powershell
pytest tests/unit -v
pytest tests/integration -v
flake8 app/
bandit -r app/ -ll
```

Las pruebas de integración se saltean cuando no están disponibles las
credenciales reales. Nunca se almacenan secretos en el repositorio.

## CI/CD

Cada `push` o Pull Request hacia `master` ejecuta Flake8, Bandit, las pruebas
unitarias, las pruebas de integración condicionadas por secretos, el contrato
OpenAPI y el build de Docker. El workflow de despliegue publica la imagen en
Artifact Registry y actualiza Cloud Run cuando está configurado el secreto
`GCP_SA_KEY` y las variables de repositorio correspondientes.
