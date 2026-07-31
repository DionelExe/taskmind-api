# Estrategia de testing

TaskMind-API aplica la pirámide de pruebas:

- **Unitarias:** validan modelos, clasificación de prioridad y endpoints con
  dependencias simuladas, sin I/O externo. Viven en `tests/unit/`.
- **Integración:** verifican conexiones reales con Firebase y Gemini cuando las
  credenciales están disponibles. Viven en `tests/integration/` y se saltean
  de forma explícita si faltan secretos.
- **Smoke/E2E de API:** el health check comprueba que la aplicación puede
  arrancar y responder mediante HTTP.

El flujo de desarrollo recomendado es TDD:

1. **Red:** escribir una prueba que falla.
2. **Green:** implementar el comportamiento mínimo.
3. **Refactor:** mejorar el código manteniendo las pruebas verdes.

Las llamadas bloqueantes de Firebase se ejecutan fuera del event loop mediante
`asyncio.to_thread`. El pipeline reconstruye temporalmente la credencial desde
`FIREBASE_CREDENTIALS_JSON` y nunca imprime su contenido.

## Ejecución local

```powershell
pytest tests/unit -v
pytest tests/integration -v
flake8 app/
bandit -r app/ -ll
```

Para ejecutar las pruebas de integración, definí `GEMINI_API_KEY` y
`GOOGLE_APPLICATION_CREDENTIALS` en el entorno. Sin ellas, pytest informa las
pruebas como `skipped` en lugar de tratarlas como fallas.

## Microservicio de notificaciones

El servicio independiente se ejecuta en `8001`. Nginx expone la API principal y
las notificaciones desde `http://localhost:8080`.

```powershell
docker compose up --build
Invoke-WebRequest http://localhost:8080/
Invoke-WebRequest http://localhost:8080/notifications `
  -Method Post -ContentType "application/json" `
  -Body '{"recipient":"test-user","title":"Prueba","message":"Smoke test"}'
```

La integración de TaskMind-API es opcional: si `NOTIFICATION_SERVICE_URL` no
está definida, la API funciona localmente sin realizar una llamada externa.
