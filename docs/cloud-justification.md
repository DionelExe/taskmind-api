# Justificación del modelo de servicio cloud

## Contexto de TaskMind-API

TaskMind-API es una API FastAPI que autentica usuarios con Firebase, clasifica
tareas mediante Google GenAI y persiste información en Firestore. El MVP tiene
un equipo pequeño, no cuenta con un rol dedicado de Operaciones y puede recibir
tráfico variable durante la validación y el crecimiento inicial.

## Alternativas consideradas

### IaaS

En Infrastructure as a Service el equipo administra máquinas virtuales,
sistema operativo, red, parches, capacidad y despliegues. Ofrece el mayor
control operativo y permite configuraciones muy específicas, pero exige
mantener servidores encendidos, dimensionar capacidad para picos y asumir el
costo y la complejidad de la operación.

### PaaS

Platform as a Service abstrae buena parte del sistema operativo y del
hardware. El proveedor administra la plataforma y el equipo se concentra en
la aplicación, aunque normalmente debe configurar capacidad, versiones,
instancias y algunos componentes de ejecución. Reduce la carga operativa frente
a IaaS, con menos control y con costos que pueden mantenerse cuando no hay
solicitudes, según el servicio elegido.

### Serverless/FaaS

Serverless permite ejecutar código sin administrar servidores. La plataforma
asigna recursos bajo demanda, escala automáticamente y factura principalmente
por el uso. En un servicio HTTP como Cloud Run, el artefacto desplegable es una
imagen de contenedor, por lo que la aplicación conserva la portabilidad de
Docker sin que el equipo administre el clúster o el sistema operativo.

## Comparación aplicada

| Criterio | IaaS | PaaS | Cloud Run (Serverless) |
| --- | --- | --- | --- |
| Control operativo | Alto; el equipo administra infraestructura y parches. | Medio; la plataforma administra la base, pero requiere configuración. | Bajo sobre infraestructura; control suficiente sobre la imagen, variables y recursos. |
| Carga para un equipo pequeño | Alta y poco conveniente para un MVP. | Media. | Baja; el proveedor gestiona capacidad, revisiones y disponibilidad. |
| Tráfico variable | Requiere sobredimensionar o automatizar grupos de instancias. | Puede escalar, según la configuración y el producto. | Escalado automático por solicitudes y concurrencia. |
| Costos sin tráfico | Una VM suele seguir generando costos mientras está encendida. | Depende del servicio y de la capacidad reservada. | El escalado a cero evita mantener instancias activas sin solicitudes. |
| Portabilidad | Depende de la imagen y de la configuración de la VM. | Puede introducir dependencia de la plataforma. | La imagen OCI permite reutilizar el mismo artefacto en otros entornos. |

## Decisión

Cloud Run es la opción más adecuada para producción del MVP porque permite
publicar la imagen Docker existente como un servicio HTTP administrado, sin
incorporar una carga de operaciones que el equipo no puede sostener. Su
escalado automático absorbe variaciones de tráfico y el **escalado a cero**
libera instancias cuando no hay solicitudes. Como consecuencia, los períodos
sin tráfico generan un ahorro de costos frente a mantener servidores o
instancias reservadas permanentemente.

Las revisiones inmutables de Cloud Run también hacen trazable cada despliegue y
facilitan un rollback. IaaS quedaría reservado para necesidades de control
sobre el sistema operativo o la red que el MVP no tiene; PaaS sería una
alternativa válida, pero Cloud Run ofrece un modelo operativo y de costos más
alineado con una API contenerizada, tráfico variable y un equipo pequeño.
