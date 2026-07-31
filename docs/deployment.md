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
python -m locust -f locustfile.py --host http://127.0.0.1:8000
```

## GitHub Actions

El workflow de [ci.yml](../.github/workflows/ci.yml) compila Python, valida
el contrato OpenAPI y construye la imagen Docker en cada Pull Request hacia
`main`. No requiere credenciales porque no ejecuta llamadas reales a Gemini
ni Firebase.

## Cloud Run

Después de autenticarte con `gcloud auth login`, configurar el proyecto y
habilitar Artifact Registry y Cloud Run, construí y publicá la imagen.

En producción, cargá las claves mediante Secret Manager o variables seguras
del servicio; no subas `.env` ni `firebase-credentials.json`.
