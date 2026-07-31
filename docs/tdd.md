# Evidencia del ciclo TDD

La funcionalidad secundaria elegida para TDD es el endpoint de readiness
`GET /health`, que permite a Docker, Cloud Run y los smoke tests comprobar que
la aplicación está disponible.

## Red

Se escribió primero `test_readiness_check_returns_ok` en
`tests/unit/test_health.py`. El test simulaba una petición HTTP a
`GET /health` y fallaba porque el endpoint todavía no existía.

## Green

Se agregó la implementación mínima en `main.py`:

```python
@app.get("/health")
async def readiness_check() -> dict[str, str]:
    return {"status": "ok"}
```

El test pasó sin realizar llamadas a Firebase, Firestore ni Gemini.

## Refactor

La respuesta se mantuvo como un contrato pequeño y estable para reutilizarla
desde el smoke test del contenedor y el despliegue en Cloud Run. La suite
unitaria continúa aislando las dependencias externas con mocks.
