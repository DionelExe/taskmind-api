# Historias de usuario

## Historia 1: Creación de tareas con priorización por IA

**Como** usuario autenticado,  
**quiero** crear una tarea con título y descripción,  
**para** que Gemini determine su prioridad y TaskMind-API la persista.

### Criterios de aceptación

- El endpoint `POST /api/v1/tasks/` requiere un Firebase ID token válido.
- La tarea se guarda con título, descripción, prioridad, fecha ISO y `owner_uid`.
- Gemini devuelve una prioridad `low`, `medium` o `high`.
- La respuesta HTTP es `201 Created` e incluye la tarea creada.
- Una solicitud sin autenticación responde `401` y no persiste datos.

## Historia 2: Autenticación de usuarios con Firebase Auth

**Como** usuario de TaskMind-API,  
**quiero** autenticar mis solicitudes con Firebase Auth,  
**para** acceder únicamente a mis tareas.

### Criterios de aceptación

- Firebase Admin SDK valida el token en cada endpoint protegido.
- Un token válido identifica al usuario mediante su UID.
- Un token ausente, inválido o expirado produce una respuesta `401`.
- Las consultas de tareas filtran por el `owner_uid` autenticado.
- La API no expone credenciales ni tokens en sus respuestas.
