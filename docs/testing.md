# Estrategia de testing

TaskMind-API aplica la pirámide de pruebas:

- **Unitarias:** validan modelos y la clasificación de prioridad sin I/O.
- **Integración:** ejercitan los endpoints FastAPI con Firebase y Gemini
  simulados.
- **Smoke/E2E de API:** el health check comprueba que la aplicación puede
  arrancar y responder mediante HTTP.

El flujo de desarrollo recomendado es TDD:

1. **Red:** escribir una prueba que falla.
2. **Green:** implementar el comportamiento mínimo.
3. **Refactor:** mejorar el código manteniendo las pruebas verdes.

Las pruebas se ejecutan sin credenciales reales. Las llamadas bloqueantes de
los SDK se mantienen aisladas y el pipeline no expone secretos.
