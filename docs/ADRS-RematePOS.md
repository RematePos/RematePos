# Architecture Decision Records (ADR) - RematePOS

Este documento contiene los registros de decisiones arquitectónicas del proyecto **RematePOS**.

Un ADR permite documentar decisiones técnicas importantes del sistema, explicando el contexto, la decisión tomada, las alternativas consideradas y sus consecuencias.

---

## Índice

| ADR | Decisión | Estado |
|---|---|---|
| ADR-001 | Arquitectura basada en microservicios | Aceptado |
| ADR-002 | Uso de API Gateway como punto único de entrada | Aceptado |
| ADR-003 | Uso de base de datos por microservicio | Aceptado |
| ADR-004 | Autenticación y autorización mediante JWT | Aceptado |
| ADR-005 | Integración de facturación con proveedor tecnológico autorizado por DIAN | Aceptado |
| ADR-006 | Dockerización de microservicios | Aceptado |
| ADR-007 | Uso de Git Flow y ramas por historia de usuario | Aceptado |
| ADR-008 | Comunicación entre frontend y backend mediante servicios por feature | Aceptado |
| ADR-009 | Manejo centralizado de errores en backend | Aceptado |
| ADR-010 | Separación progresiva de ventas, pagos, caja y facturación | Aceptado |

---

# ADR-001: Arquitectura basada en microservicios para RematePOS

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

RematePOS es un sistema POS orientado a la gestión de ventas, productos, clientes, carrito, facturación, pagos y caja. Al inicio del proyecto, varias responsabilidades podían quedar concentradas en un solo servicio, lo que dificultaría el mantenimiento, la escalabilidad y la evolución del sistema.

El proyecto necesita permitir que cada módulo pueda crecer de forma independiente. Por ejemplo, la facturación puede tener reglas propias por la integración con la DIAN; los pagos pueden integrarse con pasarelas externas; el inventario debe controlar stock; y las ventas deben manejar el flujo principal del POS.

## Decisión

Se decide implementar RematePOS usando una arquitectura basada en microservicios con Spring Boot.

Cada microservicio tendrá una responsabilidad principal dentro del sistema. La comunicación con el frontend se realizará a través de un API Gateway, evitando que React consuma directamente cada servicio interno.

Servicios principales considerados:

- auth-service: autenticación y autorización.
- customer-microservice: gestión de clientes.
- product-microservice: gestión de productos e inventario.
- cart-microservice: gestión del carrito.
- sales-service: gestión de ventas.
- payment-service: gestión de pagos.
- cash-register-service: apertura, movimientos y cierre de caja.
- billing-service o invoice-microservice: facturación POS, facturación electrónica y documentos relacionados con DIAN.
- api-gateway: punto único de entrada para el frontend.
- discovery-service: registro y descubrimiento de servicios.

## Alternativas consideradas

### Arquitectura monolítica

Ventajas:

- Más fácil de iniciar.
- Menor complejidad inicial.
- Menos configuración de red y despliegue.

Desventajas:

- Difícil de escalar por módulos.
- Mayor acoplamiento entre funcionalidades.
- Los cambios en facturación, pagos o ventas podrían afectar todo el sistema.
- Menor flexibilidad para integrar servicios externos.

### Arquitectura basada en microservicios

Ventajas:

- Mejor separación de responsabilidades.
- Permite escalar módulos específicos.
- Facilita el mantenimiento por equipos.
- Permite integrar proveedores externos de forma más ordenada.
- Mejora la organización del backend.

Desventajas:

- Mayor complejidad inicial.
- Requiere configuración de API Gateway, discovery, Docker y comunicación entre servicios.
- Puede aumentar la dificultad de pruebas integrales.

## Consecuencias

### Consecuencias positivas

- El sistema queda mejor organizado.
- Cada servicio puede evolucionar de manera independiente.
- Se facilita el trabajo por historias de usuario.
- Se mejora la mantenibilidad del proyecto.
- Se prepara el sistema para futuras integraciones, como DIAN, pagos en línea y reportes.

### Consecuencias negativas

- Se requiere mayor disciplina en configuración.
- Se deben manejar errores entre servicios.
- Se necesita documentación clara para ejecutar el sistema completo.
- El despliegue requiere más cuidado.

## Impacto en el proyecto

Esta decisión afecta directamente al backend, al frontend y al despliegue. El frontend no debe conectarse directamente a cada microservicio, sino al API Gateway. Cada microservicio debe mantener su propio dominio funcional y evitar mezclar responsabilidades.

## Relación con historias de usuario

- HU-053: Implementar API Gateway.
- HU-030: Implementar flujo POS conectado a sales-service.
- HU-025: Implementar módulo operativo de facturación POS.
- HU-019: Implementar login y configuración de acceso.

## Notas adicionales

Aunque el proyecto use microservicios, se debe evitar una separación exagerada desde el inicio. La división debe hacerse de forma incremental, manteniendo funcional el sistema en cada entrega.

---

# ADR-002: Uso de API Gateway como punto único de entrada

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

El frontend de RematePOS necesita consumir diferentes servicios backend, como clientes, productos, carrito, ventas, facturación y autenticación.

Si React consume directamente cada microservicio, se generan problemas de configuración, CORS, seguridad, rutas duplicadas y mayor dificultad para cambiar direcciones internas de servicios.

## Decisión

Se decide implementar un API Gateway como punto único de entrada HTTP para el frontend.

El frontend consumirá únicamente el API Gateway, por ejemplo:

```bash
http://localhost:8080
```

El API Gateway será responsable de enrutar las peticiones hacia los microservicios internos correspondientes.

Ejemplo:

```bash
/api/products/**   -> product-microservice
/api/customers/**  -> customer-microservice
/api/cart/**       -> cart-microservice
/api/sales/**      -> sales-service
/api/invoices/**   -> invoice-microservice
/api/auth/**       -> auth-service
```

## Alternativas consideradas

### Consumir cada microservicio directamente desde React

Ventajas:

- Configuración inicial más rápida.
- Menos componentes en el backend.

Desventajas:

- Más problemas de CORS.
- El frontend queda acoplado a la ubicación de cada servicio.
- Mayor exposición de servicios internos.
- Difícil mantenimiento cuando cambian rutas o puertos.

### Usar API Gateway

Ventajas:

- Punto único de entrada.
- Mejor control de rutas.
- Menor acoplamiento entre frontend y backend.
- Facilita seguridad, filtros, logs y manejo de CORS.
- Permite ocultar la estructura interna de microservicios.

Desventajas:

- Requiere configuración adicional.
- Si el Gateway falla, afecta el acceso general al sistema.
- Se deben mantener correctamente las rutas.

## Consecuencias

### Consecuencias positivas

- El frontend queda más limpio.
- Se centraliza la configuración de CORS.
- Se mejora la seguridad del sistema.
- Se facilita el despliegue.
- Se simplifica el consumo de servicios desde React.

### Consecuencias negativas

- El API Gateway se vuelve un componente crítico.
- Se debe monitorear su disponibilidad.
- Las rutas deben estar bien documentadas.

## Impacto en el proyecto

El frontend debe usar variables de entorno para apuntar al API Gateway. Los servicios internos no deben exponerse directamente al usuario final.

## Relación con historias de usuario

- HU-053: Implementar API Gateway.
- HU-014: Configurar frontend para entorno distribuido.
- HU-030: Implementar flujo POS conectado a sales-service.

## Notas adicionales

Toda nueva ruta backend debe ser registrada en el API Gateway antes de ser consumida por el frontend.

---

# ADR-003: Uso de base de datos por microservicio

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

RematePOS maneja diferentes dominios de información: clientes, productos, ventas, pagos, caja y facturación. Cada dominio tiene reglas propias y puede evolucionar de manera diferente.

Compartir una misma base de datos entre todos los servicios puede generar alto acoplamiento, errores por cambios en tablas y dificultad para mantener la independencia de cada microservicio.

## Decisión

Se decide que cada microservicio sea responsable de su propio modelo de datos.

Cada servicio debe administrar sus propias entidades, repositorios y migraciones de base de datos. Cuando un servicio necesite información de otro, deberá consumirla mediante API o eventos, no consultando directamente su base de datos.

## Alternativas consideradas

### Base de datos única compartida

Ventajas:

- Más fácil de consultar.
- Menor configuración inicial.
- Menos bases de datos que administrar.

Desventajas:

- Alto acoplamiento.
- Cambios en una tabla pueden afectar varios servicios.
- Rompe la independencia de los microservicios.
- Dificulta el despliegue independiente.

### Base de datos por servicio

Ventajas:

- Mayor independencia.
- Mejor separación de responsabilidades.
- Cada servicio controla su propio modelo.
- Facilita mantenimiento y escalabilidad.

Desventajas:

- Mayor complejidad en consultas cruzadas.
- Se requiere manejar consistencia entre servicios.
- Puede necesitar eventos o integración entre APIs.

## Consecuencias

### Consecuencias positivas

- Los servicios quedan menos acoplados.
- Se facilita la evolución de cada módulo.
- Cada equipo puede trabajar sobre su dominio.
- Se reducen riesgos al modificar estructuras internas.

### Consecuencias negativas

- No se deben hacer joins directos entre bases de datos de servicios diferentes.
- Se deben definir contratos claros entre servicios.
- La consistencia de datos debe manejarse con cuidado.

## Impacto en el proyecto

El backend debe evitar accesos directos a bases de datos de otros servicios. Por ejemplo, sales-service no debe consultar directamente la base de datos de product-microservice; debe consumir un endpoint o recibir eventos.

## Relación con historias de usuario

- HU-030: Implementar flujo POS conectado a sales-service.
- HU-025: Implementar módulo operativo de facturación POS.
- HU-052: Gestión de estado por módulo en frontend.

## Notas adicionales

Para operaciones críticas, como venta, pago, descuento de stock y generación de factura, se debe definir una estrategia clara de consistencia.

---

# ADR-004: Autenticación y autorización mediante JWT

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

RematePOS necesita controlar el acceso de usuarios al sistema. No todos los usuarios deben tener los mismos permisos. Por ejemplo, un cajero puede realizar ventas, pero no necesariamente administrar configuración de facturación o usuarios.

Además, el frontend necesita mantener una sesión activa después del inicio de sesión.

## Decisión

Se decide implementar autenticación mediante JWT.

Cuando el usuario inicia sesión correctamente, auth-service generará un token JWT. Este token será enviado por el frontend en cada petición protegida usando el encabezado:

```http
Authorization: Bearer <token>
```

El backend validará el token antes de permitir el acceso a recursos protegidos.

## Alternativas consideradas

### Sesiones tradicionales en servidor

Ventajas:

- Control centralizado de sesión.
- Puede ser más simple en aplicaciones pequeñas.

Desventajas:

- Menos práctico en arquitectura distribuida.
- Requiere almacenamiento de sesión.
- Puede complicar la escalabilidad.

### JWT

Ventajas:

- Funciona bien con APIs REST.
- No requiere sesión almacenada en servidor.
- Es adecuado para microservicios.
- Permite incluir roles o permisos básicos.

Desventajas:

- Si el token se filtra, puede ser usado hasta que expire.
- Requiere buen manejo de expiración.
- Debe almacenarse con cuidado en el frontend.

## Consecuencias

### Consecuencias positivas

- Se mejora la seguridad del sistema.
- El frontend puede manejar sesión de forma clara.
- Los servicios pueden validar solicitudes protegidas.
- Se permite trabajar con roles.

### Consecuencias negativas

- Se debe proteger correctamente el token.
- Se requiere definir expiración y renovación.
- Se debe evitar almacenar información sensible dentro del token.

## Impacto en el proyecto

El frontend debe guardar el token de forma controlada y enviarlo en las peticiones al API Gateway. El backend debe validar el token en rutas protegidas.

## Relación con historias de usuario

- HU-019: Implementar login conectado al auth-service.
- HU-014: Configurar frontend para entorno distribuido.

## Notas adicionales

El token no debe contener información sensible como contraseñas, datos bancarios o información privada del usuario.

---

# ADR-005: Integración de facturación electrónica y POS con proveedor tecnológico autorizado por DIAN

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

RematePOS necesita manejar facturación POS y, en una etapa posterior, facturación electrónica o documentos equivalentes electrónicos según los requerimientos de la DIAN.

Implementar una integración directa con la DIAN puede ser complejo, porque requiere manejar validaciones, XML, firmas digitales, CUFE, CUDE, QR, respuestas de validación, ambientes de prueba y certificación.

## Decisión

Se decide priorizar la integración con un proveedor tecnológico autorizado por la DIAN.

El sistema RematePOS no debe exponer al frontend la lógica sensible del proveedor tecnológico. La configuración, tokens, credenciales y comunicación con el proveedor deben manejarse desde el backend, principalmente desde billing-service o invoice-microservice.

El frontend solo debe enviar la información necesaria para solicitar la generación de la factura o documento correspondiente.

## Alternativas consideradas

### Integración directa con DIAN

Ventajas:

- Mayor control técnico.
- No depende de un proveedor externo.
- Posible reducción de costos por transacción a largo plazo.

Desventajas:

- Alta complejidad técnica.
- Mayor tiempo de implementación.
- Requiere manejo de firma digital, XML y validaciones.
- Mayor riesgo de errores legales o tributarios.

### Integración con proveedor tecnológico

Ventajas:

- Reduce complejidad técnica.
- Facilita la validación ante DIAN.
- Permite usar APIs ya preparadas.
- Puede incluir generación de PDF, XML, QR, CUFE o CUDE.
- Acelera la entrega del proyecto.

Desventajas:

- Depende de un tercero.
- Puede tener costos por transacción o plan.
- Requiere revisar documentación, límites y soporte.
- Se deben proteger tokens y credenciales.

## Consecuencias

### Consecuencias positivas

- Se acelera la implementación de facturación.
- Se reduce el riesgo técnico.
- El backend mantiene control sobre la integración.
- El frontend queda desacoplado del proveedor tecnológico.
- Se facilita el uso de ambiente sandbox.

### Consecuencias negativas

- El proyecto dependerá del proveedor seleccionado.
- Se deben evaluar costos.
- Se necesita adaptar el sistema al contrato de la API del proveedor.
- Puede haber cambios si se cambia de proveedor.

## Impacto en el proyecto

La integración con DIAN debe estar centralizada en el backend. El frontend no debe mostrar tokens, credenciales ni datos internos del proveedor. La configuración debe manejarse en variables de entorno o tablas de configuración seguras.

## Relación con historias de usuario

- HU-025: Implementar módulo operativo de facturación POS.
- HU-019: Configuración de integración con proveedor tecnológico.
- HU-030: Flujo POS conectado a ventas.

## Notas adicionales

Antes de implementar en producción, se debe validar el flujo en ambiente de pruebas del proveedor seleccionado.

---

# ADR-006: Dockerización de microservicios para entorno local y despliegue

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

RematePOS está compuesto por varios servicios backend, frontend, bases de datos y componentes de infraestructura. Ejecutar cada servicio manualmente puede generar errores de configuración, diferencias entre equipos y dificultad para probar el sistema completo.

## Decisión

Se decide dockerizar los servicios principales del proyecto usando Docker y Docker Compose.

Cada microservicio debe tener su propio Dockerfile. Además, se debe contar con un archivo docker-compose para levantar el entorno completo o parcial del sistema.

## Alternativas consideradas

### Ejecutar servicios manualmente

Ventajas:

- Más simple al inicio.
- Fácil de depurar desde el IDE.
- No requiere conocimientos avanzados de Docker.

Desventajas:

- Mayor riesgo de errores por configuración local.
- Difícil de replicar entre equipos.
- Cada integrante puede tener versiones diferentes.
- Complica despliegues futuros.

### Usar Docker y Docker Compose

Ventajas:

- Entorno más consistente.
- Facilita pruebas integrales.
- Mejora la preparación para producción.
- Permite levantar dependencias como bases de datos, discovery y gateway.
- Facilita la incorporación de nuevos integrantes.

Desventajas:

- Requiere configuración adicional.
- Puede consumir más recursos.
- Se deben mantener actualizados los Dockerfile y compose.

## Consecuencias

### Consecuencias positivas

- El entorno será más fácil de replicar.
- Se reducen errores de configuración.
- Se mejora el proceso de despliegue.
- Se facilita probar todo el flujo POS.

### Consecuencias negativas

- Se debe corregir y mantener la dockerización.
- Los integrantes deben conocer comandos básicos de Docker.
- Puede haber problemas con puertos ocupados o variables de entorno.

## Impacto en el proyecto

Cada servicio debe definir claramente sus variables de entorno, puertos y dependencias. El API Gateway debe poder comunicarse con los servicios usando los nombres definidos en Docker Compose.

## Relación con historias de usuario

- HU-053: Implementar API Gateway.
- HU-030: Flujo POS conectado a sales-service.
- HU-025: Módulo operativo de facturación POS.

## Notas adicionales

La dockerización debe validarse antes de cada entrega importante, especialmente en releases.

---

# ADR-007: Uso de Git Flow y ramas por historia de usuario

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

El equipo de RematePOS trabaja con varias historias de usuario, diferentes integrantes y múltiples repositorios. Sin una estrategia clara de ramas y commits, pueden aparecer conflictos, mezclas de funcionalidades incompletas y dificultad para revisar cambios.

## Decisión

Se decide usar un flujo basado en ramas principales y ramas hijas por historia de usuario.

Ramas principales:

- main: rama de producción.
- qa: rama de pruebas y validación.
- develop: rama principal de desarrollo.

Las ramas de trabajo deben salir desde develop y seguir el formato:

```bash
feature/HU-XX-INICIALES-short-description
```

Ejemplo:

```bash
feature/HU-030-AFAF-pos-sales-flow
feature/HU-053-CAVY-api-gateway
```

Los commits deben usar Conventional Commits en inglés.

Ejemplo:

```bash
feat(HU-030): connect POS checkout with sales service
fix(HU-053): resolve duplicated CORS configuration
docs(HU-025): update billing module documentation
```

## Alternativas consideradas

### Trabajar directamente sobre develop

Ventajas:

- Más rápido para cambios pequeños.
- Menos ramas que administrar.

Desventajas:

- Mayor riesgo de romper el proyecto.
- Dificulta la revisión de código.
- Mezcla funcionalidades incompletas.
- Complica la trazabilidad por historia de usuario.

### Usar ramas por historia de usuario

Ventajas:

- Mejor organización.
- Mayor trazabilidad.
- Facilita Pull Requests.
- Permite revisar cambios antes de fusionar.
- Reduce riesgos sobre develop.

Desventajas:

- Requiere disciplina del equipo.
- Puede generar conflictos si no se actualizan ramas.
- Necesita revisión antes de hacer merge.

## Consecuencias

### Consecuencias positivas

- Se mejora el control del código.
- Cada HU queda relacionada con una rama.
- Los commits son más claros.
- Los Pull Requests son más fáciles de revisar.
- Se reduce el riesgo de subir cambios incompletos.

### Consecuencias negativas

- Se requiere mantener ramas actualizadas.
- El equipo debe respetar el formato definido.
- Los merges deben hacerse con cuidado.

## Impacto en el proyecto

Todo integrante debe crear ramas desde develop. No se debe hacer merge hasta que la funcionalidad esté lista, probada y revisada.

## Relación con historias de usuario

Aplica para todas las historias de usuario del proyecto.

## Notas adicionales

Iniciales oficiales del equipo:

- CAVY: Carlos Andrés Villamil Yusunguaira.
- JSMV: Juan Sebastián Murcia.
- AFAF: Felipe Ardilla.
- KSCH: Kevin Santiago Cuesta.

---

# ADR-008: Comunicación entre frontend y backend mediante servicios por feature

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

El frontend de RematePOS está organizado por módulos o features, como auth, products, inventory, sales, billing y customers.

Si todas las peticiones HTTP se escriben directamente dentro de los componentes, el código se vuelve difícil de mantener, probar y reutilizar.

## Decisión

Se decide que cada feature del frontend tenga sus propios servicios para comunicarse con el backend.

Ejemplo de estructura:

```bash
src/
└── app/
    └── features/
        ├── auth/
        │   └── services/
        │       └── AuthService.js
        ├── sales/
        │   └── services/
        │       └── SalesService.js
        ├── billing/
        │   └── services/
        │       └── BillingService.js
        └── products/
            └── services/
                └── ProductService.js
```

Los componentes deben consumir estos servicios, no llamar directamente a fetch o axios sin organización.

## Alternativas consideradas

### Llamadas HTTP directamente en los componentes

Ventajas:

- Rápido para prototipos.
- Menos archivos al inicio.

Desventajas:

- Componentes más largos y difíciles de leer.
- Código repetido.
- Difícil manejo de errores.
- Baja reutilización.

### Servicios por feature

Ventajas:

- Mejor organización.
- Mayor reutilización.
- Componentes más limpios.
- Facilita pruebas y mantenimiento.
- Permite centralizar headers, token y errores.

Desventajas:

- Requiere más estructura de carpetas.
- Puede generar más archivos.
- Se debe mantener consistencia en nombres.

## Consecuencias

### Consecuencias positivas

- El frontend queda más modular.
- Se reducen duplicaciones.
- Las rutas del API Gateway quedan centralizadas.
- Se facilita cambiar endpoints.

### Consecuencias negativas

- Se debe cuidar la consistencia de nombres.
- En sistemas Windows puede haber problemas si el import no coincide con mayúsculas y minúsculas.

## Impacto en el proyecto

Cada módulo del frontend debe tener su capa de servicios. Los imports deben respetar exactamente el nombre del archivo.

Ejemplo correcto:

```js
import SalesService from "../services/SalesService";
```

Si el archivo se llama `SalesService.js`, no debe importarse como `salesService.js`.

## Relación con historias de usuario

- HU-014: Configurar frontend para entorno distribuido.
- HU-019: Implementar login.
- HU-030: Implementar flujo POS conectado a sales-service.
- HU-025: Implementar módulo operativo de facturación POS.

## Notas adicionales

Se recomienda centralizar la URL base del API Gateway usando variables de entorno.

---

# ADR-009: Manejo centralizado de errores en backend

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

Los microservicios de RematePOS deben responder errores de forma clara y consistente. Si cada controlador maneja errores de manera diferente, el frontend tendrá dificultades para mostrar mensajes adecuados al usuario.

Además, errores de validación, recursos no encontrados, errores internos o problemas de comunicación deben tener respuestas uniformes.

## Decisión

Se decide implementar manejo centralizado de errores en cada microservicio mediante un GlobalExceptionHandler.

Las respuestas de error deben tener una estructura clara, por ejemplo:

```json
{
  "timestamp": "2026-05-06T10:30:00",
  "status": 400,
  "error": "Bad Request",
  "message": "Validation error",
  "details": {
    "name": "Product name is required"
  }
}
```

## Alternativas consideradas

### Manejar errores directamente en cada controlador

Ventajas:

- Fácil de hacer al inicio.
- Permite respuestas específicas por endpoint.

Desventajas:

- Mucha repetición.
- Difícil mantenimiento.
- Respuestas inconsistentes.
- Mayor probabilidad de errores no controlados.

### Manejo centralizado con GlobalExceptionHandler

Ventajas:

- Respuestas uniformes.
- Menos código repetido.
- Mejor mantenimiento.
- Facilita el consumo desde frontend.
- Permite registrar logs de forma controlada.

Desventajas:

- Requiere diseñar una estructura común.
- Se deben crear excepciones personalizadas.
- Puede requerir ajustes por microservicio.

## Consecuencias

### Consecuencias positivas

- Mejor experiencia de usuario.
- Mayor facilidad para depurar errores.
- El frontend puede mostrar mensajes claros.
- Se reduce código duplicado.

### Consecuencias negativas

- Se debe mantener una convención común.
- Los desarrolladores deben lanzar excepciones adecuadas.

## Impacto en el proyecto

Cada microservicio debe implementar o reutilizar un manejador global de errores. El frontend debe consumir el campo `message` o `details` para mostrar alertas claras.

## Relación con historias de usuario

- HU-019: Login y manejo de errores claros.
- HU-030: Flujo POS conectado a sales-service.
- HU-025: Módulo operativo de facturación POS.

## Notas adicionales

No se deben exponer detalles técnicos sensibles al usuario final, como trazas internas, rutas del servidor o información de conexión a base de datos.

---

# ADR-010: Separación progresiva de ventas, pagos, caja y facturación

## Estado

Aceptado.

## Fecha

2026-05-06.

## Contexto

En RematePOS, el flujo de venta involucra varias responsabilidades:

- Crear la venta.
- Registrar los productos vendidos.
- Procesar el pago.
- Descontar stock.
- Registrar movimientos de caja.
- Generar factura o documento POS.
- Consultar copias de factura.
- Gestionar devoluciones.

Algunas de estas responsabilidades pueden estar inicialmente agrupadas en un mismo servicio, pero a largo plazo esto genera acoplamiento y dificultad para mantener el sistema.

## Decisión

Se decide separar progresivamente las responsabilidades en servicios especializados.

La separación objetivo será:

- sales-service: ventas y detalle de ventas.
- payment-service: pagos, referencias, estados y pasarelas.
- cash-register-service: apertura, cierre y movimientos de caja.
- billing-service o invoice-microservice: facturas, documentos POS, copias, CUFE, CUDE, QR, PDF y XML.
- product-microservice: inventario y stock.

La separación debe hacerse de forma incremental, sin romper el flujo POS que ya funciona.

## Alternativas consideradas

### Mantener todo en purchase-microservice

Ventajas:

- Menos servicios.
- Menor complejidad inicial.
- Flujo más directo.

Desventajas:

- Servicio demasiado grande.
- Mezcla ventas, pagos, caja y facturación.
- Difícil de mantener.
- Más riesgo de errores al modificar una funcionalidad.
- Dificulta integrar DIAN o pasarelas de pago.

### Separación progresiva por responsabilidades

Ventajas:

- Mejor organización.
- Servicios más claros.
- Facilita mantenimiento.
- Permite integrar proveedores externos.
- Reduce acoplamiento.

Desventajas:

- Requiere migración gradual.
- Se deben definir contratos entre servicios.
- Puede aumentar la complejidad de pruebas.

## Consecuencias

### Consecuencias positivas

- El sistema queda preparado para crecer.
- Se facilita la integración con DIAN.
- Se mejora la claridad del backend.
- Cada servicio tiene una responsabilidad concreta.
- Se facilita el trabajo del equipo por módulos.

### Consecuencias negativas

- Se necesita plan de migración.
- Puede haber duplicidad temporal durante la transición.
- Se requieren pruebas integrales del flujo POS completo.

## Impacto en el proyecto

El flujo POS debe mantenerse funcional durante toda la separación. Primero se deben estabilizar ventas, facturas reales y stock. Luego se deben separar pagos y caja sin afectar la operación principal.

## Relación con historias de usuario

- HU-030: Implementar flujo POS conectado a sales-service.
- HU-025: Implementar módulo operativo de facturación POS.
- HU-053: Implementar API Gateway.

## Notas adicionales

La separación no debe hacerse toda de una vez. Se recomienda una migración por etapas para reducir riesgos.

---

# Estados permitidos para futuros ADR

Los siguientes estados pueden utilizarse para nuevos ADR dentro del proyecto:

- Propuesto.
- Aceptado.
- Rechazado.
- Reemplazado.
- Obsoleto.

---


