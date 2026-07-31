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

```gherkin
Característica: Creación de tareas con priorización por IA

  Escenario: Crear una tarea urgente
    Dado que el usuario tiene un Firebase ID token válido
    Y proporciona un título y una descripción urgente
    Cuando envía una solicitud POST a /api/v1/tasks/
    Entonces la API responde con estado 201
    Y solicita a Gemini la clasificación de prioridad
    Y persiste la tarea asociada al UID del usuario
    Y devuelve una prioridad "high"

  Escenario: Rechazar la creación sin autenticación
    Dado que el usuario no proporciona un token válido
    Cuando envía una solicitud POST a /api/v1/tasks/
    Entonces la API responde con estado 401
    Y no almacena la tarea
```

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

```gherkin
Característica: Autenticación de usuarios con Firebase Auth

  Escenario: Autenticar una solicitud con un token válido
    Dado que Firebase Auth emitió un token válido
    Cuando el usuario solicita un recurso protegido con ese token
    Entonces Firebase Admin SDK valida el token
    Y la API identifica al usuario por su UID
    Y permite continuar la solicitud

  Escenario: Rechazar un token expirado
    Dado que el usuario envía un token expirado
    Cuando solicita un recurso protegido
    Entonces Firebase Admin SDK rechaza el token
    Y la API responde con estado 401
    Y no devuelve datos del recurso
```
