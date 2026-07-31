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

## GitHub Actions

El workflow de [ci.yml](../.github/workflows/ci.yml) ejecuta pruebas unitarias
e integración, exige un mínimo de 70% de cobertura, ejecuta Ruff, compila
Python, valida el contrato OpenAPI y construye la imagen Docker en cada Pull
Request hacia `main`. No requiere credenciales porque no ejecuta llamadas
reales a Gemini ni Firebase. La rama `main` debe exigir el check `test` y el
check `analyze` antes de permitir un merge.

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
