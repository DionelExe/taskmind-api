# Ejecución y despliegue

## Configuración local

1. Copiá `.env.example` como `.env`.
2. Completá `GEMINI_API_KEY` y `GOOGLE_APPLICATION_CREDENTIALS`.
3. Descargá la clave privada de Firebase como `firebase-credentials.json`.
4. Activá Firestore y Firebase Authentication con proveedor Correo/Contraseña.

Para ejecutar con Docker:

```powershell
docker compose up --build
```

La documentación queda disponible en `http://127.0.0.1:8000/docs`.

## Token de prueba

Completá `FIREBASE_WEB_API_KEY`, `FIREBASE_TEST_EMAIL` y
`FIREBASE_TEST_PASSWORD` en `.env`, y ejecutá:

```powershell
python get_token.py
```

Usá el token devuelto como `FIREBASE_ID_TOKEN` para una prueba de carga.

## Prueba de carga

```powershell
pip install -r requirements-dev.txt
$env:FIREBASE_ID_TOKEN = "<token>"
locust -f locustfile.py --host http://127.0.0.1:8000
```

## Testing y calidad

Las pruebas no llaman a Firebase ni a Gemini: esas integraciones se simulan
para que CI sea reproducible y no requiera secretos.

```powershell
pip install -r requirements-dev.txt
pytest --cov=app --cov-report=term-missing --cov-fail-under=70
python -m ruff check .
```

El workflow aplica el ciclo `checkout -> install -> test -> analyze -> build`.
Los jobs de Docker dependen de que tests y análisis estático terminen
correctamente. La cobertura se publica como artifact del workflow.

### SonarCloud

El repositorio incluye [sonar-project.properties](../sonar-project.properties).
Para activar el análisis, creá un proyecto en SonarCloud y agregá el token como
secret de GitHub llamado `SONAR_TOKEN`. El job se ejecuta automáticamente cuando
ese secret existe; sin él, CI continúa usando Ruff y análisis estático local.

### E2E con Docker Compose

Para verificar el microservicio real y el proxy:

```powershell
docker compose up -d --build notification-service nginx
try {
  Invoke-WebRequest http://localhost:8080/ -UseBasicParsing
  Invoke-WebRequest http://localhost:8080/notifications `
    -Method Post -ContentType "application/json" `
    -Body '{"recipient":"smoke-test","title":"Smoke","message":"OK"}' `
    -UseBasicParsing
} finally {
  docker compose down
}
```

La protección de `main` debe exigir los checks `test`, `analyze` y `container`
en Settings > Branches > Branch protection rules.

## GitHub Actions

El workflow de [ci.yml](../.github/workflows/ci.yml) ejecuta Flake8, Bandit,
Ruff, pruebas unitarias, pruebas de integración, compilación, validación del
contrato OpenAPI y construcción de Docker en cada Pull Request hacia `main`.
Las pruebas de integración se saltean si no existen secretos.

Configurá estos Repository Secrets en Settings > Secrets and variables >
Actions:

- `GEMINI_API_KEY`: clave para la prueba real contra Gemini.
- `FIREBASE_CREDENTIALS_JSON`: contenido completo de la cuenta de servicio de
  Firebase.
- `GCP_SA_KEY`: cuenta de servicio usada por el despliegue.

El workflow [cd.yml](../.github/workflows/cd.yml) publica la imagen con las
etiquetas `latest` y el SHA del commit y despliega la etiqueta inmutable en
Cloud Run. Requiere las variables de repositorio `GCP_PROJECT_ID`,
`GCP_REGION`, `GCP_ARTIFACT_REPOSITORY` y `CLOUD_RUN_SERVICE`. La protección de
`main` debe exigir los checks `quality-and-tests`, `analyze` y `container`
antes de permitir un merge.

## Cloud Run

Después de autenticarte con `gcloud auth login`, configurar el proyecto y
habilitar Artifact Registry y Cloud Run, construí y publicá la imagen:

```powershell
gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT_ID/taskmind-api/api
gcloud run deploy taskmind-api `
  --image REGION-docker.pkg.dev/PROJECT_ID/taskmind-api/api `
  --region REGION `
  --allow-unauthenticated
```

En producción, cargá las claves mediante Secret Manager o variables seguras
del servicio; no subas `.env` ni `firebase-credentials.json`.
