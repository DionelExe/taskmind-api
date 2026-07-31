# Historias de usuario

## Historia 1: Creación de Tareas con Priorización por IA

### Descripción

**Como** usuario autenticado,  
**quiero** crear una tarea describiendo su objetivo y contexto,  
**para** que TaskMind-API la almacene y determine automáticamente si su prioridad es
BAJA, MEDIA o ALTA mediante Gemini.

### Criterios de aceptación

- La solicitud debe requerir autenticación válida mediante Firebase Auth.
- La tarea debe almacenar su descripción, fecha de creación y usuario propietario.
- Gemini debe clasificar la prioridad como `BAJA`, `MEDIA` o `ALTA`.
- La respuesta debe devolver la tarea creada junto con su prioridad.
- Si la clasificación no está disponible, la API debe informar el error sin confirmar
  una tarea incompleta.

### Escenarios

```gherkin
Característica: Creación de tareas con priorización por IA

  Escenario: Crear una tarea y clasificarla como alta prioridad
    Dado que el usuario tiene un token válido de Firebase Auth
    Y proporciona una descripción de tarea urgente
    Cuando envía una solicitud POST al endpoint de creación de tareas
    Entonces la API almacena la tarea asociada al usuario
    Y solicita a Gemini la clasificación de prioridad
    Y responde con la prioridad "ALTA"
    Y devuelve la tarea creada.

  Escenario: Rechazar la creación sin autenticación
    Dado que el usuario no proporciona un token válido
    Cuando envía una solicitud POST al endpoint de creación de tareas
    Entonces la API responde con estado 401
    Y no almacena la tarea.
```

## Historia 2: Autenticación de Usuarios con Firebase Auth

### Descripción

**Como** usuario de TaskMind-API,  
**quiero** autenticarme con Firebase Auth,  
**para** acceder únicamente a mis tareas y mantener protegida mi información.

### Criterios de aceptación

- Firebase Admin SDK debe validar el token Bearer enviado en cada endpoint protegido.
- Un token válido debe identificar al usuario autenticado.
- Un token ausente, inválido o expirado debe producir una respuesta 401.
- Las tareas consultadas o modificadas deben pertenecer al usuario autenticado.
- La API no debe exponer credenciales ni tokens en sus respuestas.

### Escenarios

```gherkin
Característica: Autenticación de usuarios con Firebase Auth

  Escenario: Autenticar una solicitud con un token válido
    Dado que Firebase Auth emitió un token Bearer vigente
    Cuando el usuario solicita un recurso protegido con ese token
    Entonces Firebase Admin SDK valida el token
    Y la API identifica al usuario por su UID
    Y permite continuar la solicitud.

  Escenario: Rechazar un token expirado
    Dado que el usuario envía un token Bearer expirado
    Cuando solicita un recurso protegido
    Entonces Firebase Admin SDK rechaza el token
    Y la API responde con estado 401
    Y no devuelve datos del recurso.
```
