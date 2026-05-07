# ADRs Aplicados por Historia de Usuario

## Proposito del documento

Este documento evidencia como los Architectural Decision Records (ADRs) se aplican realmente en RematePOS mediante historias de usuario, ramas feature, commits convencionales, repositorios y evidencias funcionales.

La intencion no es solo listar decisiones arquitectonicas. Cada ADR debe poder trazarse asi:

```text
ADR -> HU -> rama feature -> commits -> repositorio -> evidencia funcional -> estado
```

Esta trazabilidad permite revisar si una decision ya fue aplicada, esta en implementacion o sigue pendiente para una fase posterior.

## Equipo e iniciales oficiales

| Responsabilidad | Integrante | Iniciales oficiales | ADRs a cargo |
| --- | --- | --- | --- |
| Backend | Carlos Andrés Villamil Yusunguaira | `CAVY` | ADR-001, ADR-004, ADR-005, ADR-006, ADR-007 |
| PO | Kevin Santiago Cuesta Hernández | `KSCH` | ADR-002, ADR-003, ADR-008, ADR-009, ADR-010 |
| Frontend | Andrés Felipe Ardila Fajardo | `AFAF` | ADR-012, ADR-013, ADR-014, ADR-015, ADR-016 |
| QA | Juan Sebastián Murcia Vargas | `JSMV` | ADR-011, ADR-017, ADR-018, ADR-019, ADR-020 |

## Catálogo oficial de ADRs

### ADR-001 - Adoptar arquitectura por capas / hexagonal ligera en cada microservicio

| Campo | Valor |
| --- | --- |
| Responsable | Carlos Andrés Villamil Yusunguaira |
| Tipo | Patrón estructural |
| Estado | Propuesto |

**Contexto:** El microservicio de productos puede crecer rápido. Si se mezcla controlador, lógica de negocio y acceso a datos en la misma clase, mantenerlo luego será más difícil.

**Decisión:** Separar cada microservicio en capas claras: controller, application/service, domain, infrastructure/repository.

**Impacto:** Mejora mantenibilidad, pruebas y orden del código. Como costo, toca reorganizar clases actuales.

**Aplicación en RematePOS:** Mover la lógica del microservicio de productos para que el controller solo reciba y responda. La lógica queda en servicios de aplicación y el acceso a datos en repositorios.

### ADR-002 - Usar API Gateway como punto único de entrada

| Campo | Valor |
| --- | --- |
| Responsable | Kevin Santiago Cuesta Hernández |
| Tipo | Patrón estructural |
| Estado | Propuesto |

**Contexto:** Si el sistema va a tener varios microservicios, no conviene que el frontend consuma cada uno por separado.

**Decisión:** Centralizar el acceso mediante un API Gateway.

**Impacto:** Facilita seguridad, rutas, control de tráfico y una sola entrada para frontend. Como costo, agrega una pieza más a desplegar.

**Aplicación en RematePOS:** El frontend deja de llamar directo a productos y en su lugar consume el Gateway. Más adelante allí pueden ir auth, rate limiting y enrutamiento.

### ADR-003 - Base de datos por microservicio

| Campo | Valor |
| --- | --- |
| Responsable | Kevin Santiago Cuesta Hernández |
| Tipo | Patrón estructural |
| Estado | Propuesto |

**Contexto:** Cuando se empieza, da tentación poner todos los módulos sobre una sola base. Eso rompe la independencia entre servicios.

**Decisión:** Cada microservicio tendrá su propia base de datos o al menos su propio esquema independiente, sin acceso directo entre ellos.

**Impacto:** Mejora autonomía, escalabilidad y reduce acoplamiento. Como costo, complica un poco consultas cruzadas.

**Aplicación en RematePOS:** Productos maneja sus datos. Si luego nace inventario o ventas, no deberían leer tablas de productos directamente.

### ADR-004 - No exponer entidades directamente; usar DTOs

| Campo | Valor |
| --- | --- |
| Responsable | Carlos Andrés Villamil Yusunguaira |
| Tipo | Patrón de diseño |
| Estado | Propuesto |

**Contexto:** Devolver entidades JPA al frontend genera acoplamiento, fugas de datos y problemas al cambiar el modelo interno.

**Decisión:** Todas las entradas y salidas de API se harán con DTOs.

**Impacto:** Mejor control de contrato, seguridad y estabilidad de la API. Como costo, hay que crear clases extra y mapeadores.

**Aplicación en RematePOS:** En productos, crear por ejemplo `ProductRequestDTO`, `ProductResponseDTO`, `ProductListDTO`.

### ADR-005 - Validación de datos en backend con Bean Validation

| Campo | Valor |
| --- | --- |
| Responsable | Carlos Andrés Villamil Yusunguaira |
| Tipo | Patrón de diseño |
| Estado | Propuesto |

**Contexto:** No se puede confiar solo en el frontend para validar datos como nombre, precio, stock o código.

**Decisión:** Aplicar validaciones con anotaciones como `@NotBlank`, `@NotNull`, `@Positive`, `@Size`.

**Impacto:** Evita datos inválidos en la base y hace la API más robusta. Como costo, toca definir bien reglas y mensajes.

**Aplicación en RematePOS:** Validar creación y edición de productos, por ejemplo nombre obligatorio, precio mayor que cero, stock no negativo.

### ADR-006 - Manejo global de errores con @RestControllerAdvice

| Campo | Valor |
| --- | --- |
| Responsable | Carlos Andrés Villamil Yusunguaira |
| Tipo | Patrón comportamental |
| Estado | Propuesto |

**Contexto:** Si cada controller maneja errores distinto, la API queda inconsistente.

**Decisión:** Centralizar excepciones en un manejador global que devuelva respuestas uniformes.

**Impacto:** Errores más claros para frontend y menos repetición de código. Como costo, toca definir estructura estándar de error.

**Aplicación en RematePOS:** Crear respuestas tipo: timestamp, status, error, message, path.

### ADR-007 - Delimitar transacciones en capa de servicio

| Campo | Valor |
| --- | --- |
| Responsable | Carlos Andrés Villamil Yusunguaira |
| Tipo | Patrón comportamental |
| Estado | Propuesto |

**Contexto:** Operaciones como crear producto, actualizar stock o registrar cambios deben ejecutarse completas o no ejecutarse.

**Decisión:** Usar `@Transactional` en métodos de servicio, no en controllers.

**Impacto:** Protege la consistencia de datos. Como costo, toca revisar bien qué métodos son transaccionales y cuáles no.

**Aplicación en RematePOS:** Aplicarlo en creación, actualización, cambios de estado y operaciones que toquen más de una entidad.

### ADR-008 - Implementar patrón Specification o filtros dinámicos para consultas

| Campo | Valor |
| --- | --- |
| Responsable | Kevin Santiago Cuesta Hernández |
| Tipo | Patrón de diseño |
| Estado | Propuesto |

**Contexto:** En productos normalmente aparecen filtros por nombre, categoría, precio, disponibilidad, estado, etc.

**Decisión:** Construir filtros dinámicos reutilizables en vez de llenar repositorios con muchos métodos específicos.

**Impacto:** Consultas más limpias y escalables. Como costo, requiere una capa de filtrado un poco más elaborada.

**Aplicación en RematePOS:** Buscar productos por combinaciones como nombre + rango de precio + activos + stock disponible.

### ADR-009 - Comunicación entre microservicios orientada a eventos

| Campo | Valor |
| --- | --- |
| Responsable | Kevin Santiago Cuesta Hernández |
| Tipo | Patrón comportamental |
| Estado | Propuesto |

**Contexto:** Cuando el sistema crezca, no todo debería resolverse con llamadas HTTP entre servicios.

**Decisión:** Usar eventos de dominio para acciones importantes, por ejemplo: ProductoCreado, StockActualizado, VentaRegistrada.

**Impacto:** Reduce acoplamiento y facilita escalabilidad. Como costo, aumenta la complejidad de infraestructura.

**Aplicación en RematePOS:** Cuando se registre una venta, otro servicio puede reaccionar y descontar stock o generar auditoría sin acoplamiento fuerte.

### ADR-010 - Usar patrón Outbox para publicación confiable de eventos

| Campo | Valor |
| --- | --- |
| Responsable | Kevin Santiago Cuesta Hernández |
| Tipo | Patrón de diseño |
| Estado | Propuesto |

**Contexto:** Si se guarda información en base de datos pero falla la publicación del evento, el sistema queda inconsistente.

**Decisión:** Guardar eventos en una tabla Outbox dentro de la misma transacción y luego publicarlos de forma segura.

**Impacto:** Mejora confiabilidad entre base de datos y mensajería. Como costo, añade una tabla y un proceso publicador.

**Aplicación en RematePOS:** Especialmente útil cuando entren ventas, inventario, facturación y sincronización entre servicios.

### ADR-011 - Configuración externa por ambiente y uso de perfiles

| Campo | Valor |
| --- | --- |
| Responsable | Juan Sebastián Murcia Vargas |
| Tipo | Patrón estructural |
| Estado | Propuesto |

**Contexto:** No conviene dejar URLs, puertos, credenciales o configuraciones quemadas en código.

**Decisión:** Manejar configuración por perfiles: dev, test, prod.

**Impacto:** Facilita despliegues y reduce errores por ambiente. Como costo, hay que ordenar archivos de configuración.

**Aplicación en RematePOS:** Separar configuración de base de datos, puertos, logs, JWT, CORS y endpoints externos.

### ADR-012 - Documentar la API con OpenAPI/Swagger

| Campo | Valor |
| --- | --- |
| Responsable | Andrés Felipe Ardila Fajardo |
| Tipo | Patrón estructural |
| Estado | Propuesto |

**Contexto:** Frontend y backend necesitan hablar el mismo idioma. Si no hay documentación, aparecen malos entendidos.

**Decisión:** Documentar todos los endpoints con OpenAPI.

**Impacto:** Mejora comunicación del equipo y pruebas manuales. Como costo, exige mantener la documentación actualizada.

**Aplicación en RematePOS:** Documentar endpoints de productos: listar, crear, editar, eliminar, buscar, filtrar.

### ADR-013 - Organizar el frontend por módulos o features

| Campo | Valor |
| --- | --- |
| Responsable | Andrés Felipe Ardila Fajardo |
| Tipo | Patrón estructural |
| Estado | Propuesto |

**Contexto:** Si el frontend se organiza por tipo de archivo solamente, luego cuesta mucho encontrar y mantener cosas.

**Decisión:** Separar el frontend por dominios funcionales: productos, ventas, inventario, auth, shared.

**Impacto:** Mejora orden, escalabilidad y trabajo en equipo. Como costo, toca mover estructura actual si está desordenada.

**Aplicación en RematePOS:** El módulo de productos debe contener sus vistas, servicios, modelos, rutas y componentes propios.

### ADR-014 - Crear librería de componentes compartidos

| Campo | Valor |
| --- | --- |
| Responsable | Andrés Felipe Ardila Fajardo |
| Tipo | Patrón estructural |
| Estado | Propuesto |

**Contexto:** Botones, tablas, inputs, modales, alertas y loaders suelen repetirse mucho.

**Decisión:** Centralizar componentes reutilizables en un módulo shared o una pequeña librería interna.

**Impacto:** Disminuye duplicación y mejora consistencia visual. Como costo, toca invertir tiempo en abstraer componentes.

**Aplicación en RematePOS:** Crear componentes reutilizables para tabla de productos, formularios, confirmación de borrado, paginación y mensajes.

### ADR-015 - Autenticación y autorización con JWT y guards

| Campo | Valor |
| --- | --- |
| Responsable | Andrés Felipe Ardila Fajardo |
| Tipo | Patrón comportamental |
| Estado | Propuesto |

**Contexto:** Un POS necesita restringir acceso según roles: admin, cajero, bodega, etc.

**Decisión:** Usar JWT para autenticación y guards/interceptors para proteger rutas y peticiones.

**Impacto:** Mejora seguridad y control de acceso. Como costo, implica flujo adicional de login, refresh y manejo de sesión.

**Aplicación en RematePOS:** Proteger módulos sensibles como inventario, reportes, cierres de caja y administración de usuarios.

### ADR-016 - Manejo de estado del frontend por feature

| Campo | Valor |
| --- | --- |
| Responsable | Andrés Felipe Ardila Fajardo |
| Tipo | Patrón comportamental |
| Estado | Propuesto |

**Contexto:** Cuando el frontend crece, manejar estado de tablas, filtros, formularios y respuestas sueltas se vuelve caótico.

**Decisión:** Usar un patrón de estado por módulo, con servicios/store por feature.

**Impacto:** Hace más predecible el comportamiento de la interfaz. Como costo, hay una curva inicial de organización.

**Aplicación en RematePOS:** En productos, manejar desde un store o servicio central: listado, filtro, loading, error, paginación y selección.

### ADR-017 - Logging estructurado y trazabilidad con correlation ID

| Campo | Valor |
| --- | --- |
| Responsable | Juan Sebastián Murcia Vargas |
| Tipo | Patrón comportamental |
| Estado | Propuesto |

**Contexto:** En microservicios, cuando algo falla, seguir la pista de una solicitud puede ser difícil.

**Decisión:** Implementar logs estructurados e incluir un correlationId por petición.

**Impacto:** Facilita depuración y monitoreo. Como costo, toca ajustar filtros, interceptores y formato de logs.

**Aplicación en RematePOS:** Cada request al sistema debe poder rastrearse desde gateway hasta el microservicio afectado.

### ADR-018 - Estandarizar ejecución local con Docker Compose

| Campo | Valor |
| --- | --- |
| Responsable | Juan Sebastián Murcia Vargas |
| Tipo | Patrón estructural |
| Estado | Propuesto |

**Contexto:** Cuando cada integrante levanta el proyecto distinto, aparecen errores de "en mi máquina sí funciona".

**Decisión:** Levantar servicios base con Docker Compose.

**Impacto:** Mejora reproducibilidad y acelera integración del equipo. Como costo, hay que preparar contenedores y variables de entorno.

**Aplicación en RematePOS:** Levantar backend, base de datos, gateway y herramientas auxiliares desde un solo comando.

### ADR-019 - Pipeline de CI con pruebas y reglas mínimas de calidad

| Campo | Valor |
| --- | --- |
| Responsable | Juan Sebastián Murcia Vargas |
| Tipo | Patrón de diseño |
| Estado | Propuesto |

**Contexto:** Si el equipo sube cambios sin controles, se rompen ramas fácilmente.

**Decisión:** Configurar pipeline para ejecutar pruebas, validación de build y análisis básico antes de merge.

**Impacto:** Mejora calidad y evita errores tempranos. Como costo, requiere preparar scripts y tiempo de integración.

**Aplicación en RematePOS:** Al menos correr build, test unitarios, lint y validación de cobertura mínima.

### ADR-020 - Usar caché para consultas de catálogo de productos

| Campo | Valor |
| --- | --- |
| Responsable | Juan Sebastián Murcia Vargas |
| Tipo | Patrón de diseño |
| Estado | Propuesto |

**Contexto:** Las consultas de productos suelen leerse mucho más de lo que se escriben.

**Decisión:** Cachear consultas frecuentes como listado de productos, categorías o catálogos.

**Impacto:** Mejora rendimiento y reduce carga en base de datos. Como costo, toca invalidar caché cuando haya actualizaciones.

**Aplicación en RematePOS:** Aplicar caché a listados o búsquedas frecuentes del catálogo, especialmente si luego el sistema tendrá muchas consultas.

## Estados usados

| Estado | Significado |
| --- | --- |
| Aplicado | La decision ya tiene HU, rama, commits y evidencia funcional. |
| En implementacion | La decision ya tiene HU o rama definida, pero aun requiere cerrar implementacion o pruebas. |
| Pendiente | La decision requiere una HU nueva o aun no tiene evidencia suficiente. |
| Planeado | La decision forma parte del roadmap aprobado, pero no debe implementarse todavia. |

## Evidencia aplicada confirmada

### ADR-002 - API Gateway

ADR-002 ya esta aplicado mediante la HU-053.

| Campo | Evidencia |
| --- | --- |
| HU | `HU-053` |
| Rama feature | `feature/HU-053-CAVY-api-gateway` |
| Repositorio | `RematePos-api` |
| Responsable ADR | Kevin Santiago Cuesta Hernández (`KSCH`) |
| Ejecución técnica HU-053 | Carlos Andrés Villamil Yusunguaira (`CAVY`) |
| Evidencia funcional | API Gateway standalone, rutas configuradas, CORS corregido, README actualizado y PR Draft hacia `develop`. |
| Commits | `feat(HU-053): add API Gateway Spring Boot project`; `feat(HU-053): configure backend service routes`; `fix(HU-053): resolve duplicated CORS configuration`; `chore(HU-053): configure gateway environment variables`; `docs(HU-053): update API Gateway README` |
| Estado | Aplicado |

## Matriz general ADR - HU - evidencia

| ADR | Decision arquitectonica | Responsable | HU relacionada | Rama feature | Repositorio | Commits relacionados | Evidencia funcional | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADR-001 | Arquitectura por capas / hexagonal ligera en cada microservicio | CAVY | HU-11, HU-12, HU-66 | `feature/HU-66-CAVY-purchase-service-split-plan` | RematePos-Backend | Por cerrar en HU-66 | Microservicios separados por controller, service, repository, dto/model y clients | En implementacion |
| ADR-002 | API Gateway como punto único de entrada | KSCH | HU-053 | `feature/HU-053-CAVY-api-gateway` | RematePos-api | `feat`, `fix`, `chore`, `docs` de HU-053 | Gateway standalone en `:8080`, rutas a microservicios, CORS corregido | Aplicado |
| ADR-003 | Base de datos por microservicio | KSCH | HU-13, HU-060, HU-82 | `feature/HU-82-CAVY-environment-strategy` | RematePos-bd / RematePos-Backend | Por cerrar en HU-82 | Ambientes y esquemas independientes identificados | En implementacion |
| ADR-004 | DTOs para entrada y salida de API | CAVY | HU-28, HU-33, HU-61 | `feature/HU-61-CAVY-payment-model` | RematePos-Backend | Por cerrar en HU-61 | Contratos de checkout, pago, webhook, compra y factura separados del modelo interno | En implementacion |
| ADR-005 | Bean Validation en backend | CAVY | HU-22, HU-28, HU-62 | `feature/HU-62-CAVY-cash-payment-flow` | RematePos-Backend | Por cerrar en HU-62 | Validaciones de producto, cantidad, pago y montos | En implementacion |
| ADR-006 | Manejo global de errores con `@RestControllerAdvice` | CAVY | HU-35, HU-37, HU-38 | `feature/HU-35-CAVY-invoice-recent-endpoint` | RematePos-Backend | Por cerrar en HU-35 / HU-38 | Factura inexistente responde `404`; errores distribuidos pendientes de estandarizacion completa | En implementacion |
| ADR-007 | Transacciones en capa de servicio | CAVY | HU-65 | `feature/HU-65-CAVY-sync-payment-sale-inventory-invoice` | RematePos-Backend | Por cerrar en HU-65 | Pago aprobado coordina venta, inventario y factura desde service layer | En implementacion |
| ADR-008 | Specification / filtros dinámicos para consultas | KSCH | HU-055 | `feature/HU-055-CAVY-dynamic-product-filters` | RematePos-Backend | Pendiente | Filtros escalables para productos por nombre, categoría, precio, disponibilidad y estado | Pendiente |
| ADR-009 | Comunicación entre microservicios orientada a eventos | KSCH | HU-054, HU-67, HU-68, HU-69 | `feature/HU-054-CAVY-event-driven-communication` | RematePos-Backend | Planeado | Separacion futura de purchase-service mediante eventos de dominio | Planeado |
| ADR-010 | Outbox para publicación confiable de eventos | KSCH | HU-085 | `feature/HU-085-CAVY-outbox-transaction-pattern` | RematePos-Backend | Pendiente | Consistencia eventual para pagos, inventario y facturación cuando existan eventos | Pendiente |
| ADR-011 | Configuración externa por ambiente y perfiles | JSMV | HU-056, HU-057, HU-082 | `feature/HU-82-CAVY-environment-strategy` | RematePos-Backend / RematePos-api | Por cerrar en HU-82 | Variables de entorno, perfiles dev/qa/main y configuración por servicio | En implementacion |
| ADR-012 | OpenAPI / Swagger | AFAF | HU-086 | `feature/HU-086-AFAF-openapi-documentation` | RematePos-Backend / RematePos-api | Pendiente | Contratos API consumibles por frontend, QA y Postman | Pendiente |
| ADR-013 | Frontend por módulos o features | AFAF | HU-050, HU-30, HU-35 | `feature/HU-050-AFAF-frontend-feature-structure` | RematePos-Frontend | Por cerrar en HU-050 | Features como sales, billing, inventory y customers | En implementacion |
| ADR-014 | Librería de componentes compartidos | AFAF | HU-051 | `feature/HU-051-AFAF-shared-components-library` | RematePos-Frontend | Pendiente | Componentes compartidos para botones, formularios, tablas, alertas y paginación | Pendiente |
| ADR-015 | JWT y guards | AFAF | HU-17, HU-73, HU-74, HU-75 | `feature/HU-073-AFAF-frontend-visual-security` | RematePos-Frontend / RematePos-api / RematePos-Backend | Planeado | Seguridad visual, guards, interceptors y protección futura de endpoints | Planeado |
| ADR-016 | Estado frontend por feature | AFAF | HU-052, HU-30, HU-35 | `feature/HU-052-AFAF-feature-state-management` | RematePos-Frontend | Pendiente | Estado de carrito, productos, factura, loading, error y paginación por feature | Pendiente |
| ADR-017 | Logging estructurado y correlation ID | JSMV | HU-087 | `feature/HU-087-JSMV-structured-logging-correlation-id` | RematePos-Backend / RematePos-api | Pendiente | Trazabilidad desde Gateway hasta microservicios | Pendiente |
| ADR-018 | Docker Compose local | JSMV | HU-057, HU-083 | `feature/HU-083-CAVY-rematepos-docker-compose` | RematePos-Backend / RematePos-api / RematePos-bd | Por cerrar en HU-083 | Ejecución local reproducible del ecosistema RematePOS | En implementacion |
| ADR-019 | Pipeline CI con pruebas y reglas mínimas | JSMV | HU-058, HU-079, HU-080 | `feature/HU-058-JSMV-continuous-integration-pipeline` | Todos los repos | Pendiente | Build, tests, lint y validaciones antes de merge | Pendiente |
| ADR-020 | Caché para catálogo de productos | JSMV | HU-088 | `feature/HU-088-JSMV-product-catalog-cache` | RematePos-Backend | Pendiente | Cache para consultas frecuentes de productos y categorías | Pendiente |

## Relacion de ADRs con HUs y repositorios

| ADR | HU relacionada | Rama feature esperada | Repositorio correcto | Estado |
| --- | --- | --- | --- | --- |
| ADR-001 | HU-11, HU-12, HU-66 | `feature/HU-66-CAVY-purchase-service-split-plan` | RematePos-Backend | En implementacion |
| ADR-002 | HU-053 | `feature/HU-053-CAVY-api-gateway` | RematePos-api | Aplicado |
| ADR-003 | HU-13, HU-060, HU-82 | `feature/HU-82-CAVY-environment-strategy` | RematePos-bd / RematePos-Backend | En implementacion |
| ADR-004 | HU-28, HU-33, HU-61 | `feature/HU-61-CAVY-payment-model` | RematePos-Backend | En implementacion |
| ADR-005 | HU-22, HU-28, HU-62 | `feature/HU-62-CAVY-cash-payment-flow` | RematePos-Backend | En implementacion |
| ADR-006 | HU-37, HU-38, HU-35 | `feature/HU-35-CAVY-invoice-recent-endpoint` | RematePos-Backend | En implementacion |
| ADR-007 | HU-65 | `feature/HU-65-CAVY-sync-payment-sale-inventory-invoice` | RematePos-Backend | En implementacion |
| ADR-008 | HU-055 | `feature/HU-055-CAVY-dynamic-product-filters` | RematePos-Backend | Pendiente |
| ADR-009 | HU-054, HU-67, HU-68, HU-69 | `feature/HU-054-CAVY-event-driven-communication` | RematePos-Backend | Planeado |
| ADR-010 | HU-085 | `feature/HU-085-CAVY-outbox-transaction-pattern` | RematePos-Backend | Pendiente |
| ADR-011 | HU-056, HU-057, HU-082 | `feature/HU-82-CAVY-environment-strategy` | RematePos-Backend / RematePos-api | En implementacion |
| ADR-012 | HU-086 | `feature/HU-086-AFAF-openapi-documentation` | RematePos-Backend / RematePos-api | Pendiente |
| ADR-013 | HU-050 | `feature/HU-050-AFAF-frontend-feature-structure` | RematePos-Frontend | En implementacion |
| ADR-014 | HU-051 | `feature/HU-051-AFAF-shared-components-library` | RematePos-Frontend | Pendiente |
| ADR-015 | HU-017, HU-073, HU-074, HU-075 | `feature/HU-075-CAVY-protect-private-endpoints-with-jwt` | RematePos-Backend / RematePos-api / RematePos-Frontend | Planeado |
| ADR-016 | HU-052 | `feature/HU-052-AFAF-feature-state-management` | RematePos-Frontend | Pendiente |
| ADR-017 | HU-087 | `feature/HU-087-JSMV-structured-logging-correlation-id` | RematePos-Backend / RematePos-api | Pendiente |
| ADR-018 | HU-057, HU-083 | `feature/HU-083-CAVY-rematepos-docker-compose` | RematePos-Backend / RematePos-api / RematePos-bd | En implementacion |
| ADR-019 | HU-058 | `feature/HU-058-JSMV-continuous-integration-pipeline` | Todos los repos | Pendiente |
| ADR-020 | HU-088 | `feature/HU-088-JSMV-product-catalog-cache` | RematePos-Backend | Pendiente |

## HUs en implementacion relacionadas

| HU | Alcance | ADRs relacionados | Repositorio |
| --- | --- | --- | --- |
| HU-30 | Flujo POS frontend conectado a backend/gateway | ADR-013, ADR-016 | RematePos-Frontend |
| HU-35 | Consumir invoice-service desde POS | ADR-004, ADR-006, ADR-013 | RematePos-Frontend / RematePos-Backend |
| HU-53 | API Gateway | ADR-002, ADR-011 | RematePos-api |
| HU-56 | Configuracion externa por ambiente | ADR-011 | RematePos-Backend / RematePos-api |
| HU-57 | Docker Compose entorno local | ADR-018 | RematePos-Backend |
| HU-61 | Modelo de pagos por venta | ADR-004, ADR-007 | RematePos-Backend |
| HU-62 | Pago en efectivo | ADR-005, ADR-007 | RematePos-Backend |
| HU-63 | Movimiento basico de caja | ADR-003, ADR-007 | RematePos-Backend / RematePos-bd |
| HU-64 | Pasarela sandbox | ADR-009 | RematePos-Backend |
| HU-65 | Sincronizar pago, venta, inventario y factura | ADR-007, ADR-009 | RematePos-Backend |
| HU-66 | Preparar separacion futura de purchase-microservice | ADR-001, ADR-009 | RematePos-Backend / RematePos |
| HU-72 | Estandarizar ramas y commits | Gobierno documental de ADRs y HUs | RematePos |
| HU-73 | Seguridad visual frontend | ADR-015 | RematePos-Frontend |
| HU-74 | Persistencia y expiracion de sesion | ADR-015, ADR-016 | RematePos-Frontend |
| HU-75 | Proteger endpoints privados con JWT | ADR-015 | RematePos-Backend / RematePos-api |
| HU-76 | Manifest y estabilidad frontend | ADR-013 | RematePos-Frontend |
| HU-77 | Fortalecer backend de devoluciones | ADR-006, ADR-007 | RematePos-Backend |
| HU-78 | Fortalecer frontend de devoluciones | ADR-013, ADR-016 | RematePos-Frontend |
| HU-79 | Plan de pruebas funcionales POS | ADR-019 | RematePos |
| HU-80 | Validar flujo completo venta-pago-factura | ADR-007, ADR-019 | RematePos |
| HU-81 | Criterios de aceptacion por HU | ADR-001 a ADR-020 | RematePos |
| HU-82 | Ambientes DEV, QA y produccion | ADR-003, ADR-011, ADR-018 | RematePos-Backend / RematePos-bd |
| HU-83 | Docker Compose ecosistema RematePOS | ADR-018 | RematePos-Backend / RematePos-api / RematePos-bd |
| HU-84 | Documentar ADRs aplicados por HU | ADR-001 a ADR-020 | RematePos |

## ADRs por integrante

### Backend - Carlos Andrés Villamil Yusunguaira - CAVY

| ADR | Decision | HU / rama | Repositorio | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- |
| ADR-001 | Arquitectura por capas / hexagonal ligera | HU-11, HU-12, HU-66 / `feature/HU-66-CAVY-purchase-service-split-plan` | RematePos-Backend | Microservicios Spring Boot separados por controller, service, repository, dto, model y client. | En implementacion |
| ADR-004 | Uso de DTOs | HU-28, HU-33, HU-61 / `feature/HU-61-CAVY-payment-model` | RematePos-Backend | DTOs para checkout, pago, webhook, respuesta de compra y factura. | En implementacion |
| ADR-005 | Bean Validation | HU-22, HU-28, HU-62 / `feature/HU-62-CAVY-cash-payment-flow` | RematePos-Backend | Validaciones de request para producto, cantidad, pago y montos. | En implementacion |
| ADR-006 | Manejo global de errores | HU-35, HU-37, HU-38 / `feature/HU-35-CAVY-invoice-recent-endpoint` | RematePos-Backend | Factura inexistente responde `404` y no `500`; errores distribuidos siguen pendientes de estandarizacion completa. | En implementacion |
| ADR-007 | Transacciones en capa de servicio | HU-65 / `feature/HU-65-CAVY-sync-payment-sale-inventory-invoice` | RematePos-Backend | Venta, pago, descuento de inventario y factura se coordinan desde service layer. | En implementacion |

### PO - Kevin Santiago Cuesta Hernández - KSCH

| ADR | Decision | HU / rama | Repositorio | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- |
| ADR-002 | API Gateway | HU-053 / `feature/HU-053-CAVY-api-gateway` | RematePos-api | Gateway standalone, rutas a microservicios, CORS corregido, README y PR Draft hacia `develop`. | Aplicado |
| ADR-003 | Base de datos por microservicio | HU-13, HU-060, HU-82 / `feature/HU-82-CAVY-environment-strategy` | RematePos-bd / RematePos-Backend | Ambientes independientes y migraciones versionadas estan identificados. | En implementacion |
| ADR-008 | Specification / filtros dinamicos | HU-055 / `feature/HU-055-CAVY-dynamic-product-filters` | RematePos-Backend | Requiere HU dedicada para filtros escalables en catalogo. | Pendiente |
| ADR-009 | Comunicacion orientada a eventos | HU-054, HU-67, HU-68, HU-69 | RematePos-Backend | Planeado para separar purchase-service en sales/payment/cash-register/billing. | Planeado |
| ADR-010 | Outbox | HU-085 / `feature/HU-085-CAVY-outbox-transaction-pattern` | RematePos-Backend | Requiere HU nueva para garantizar consistencia eventual entre pago, inventario y facturacion. | Pendiente |

### Frontend - Andrés Felipe Ardila Fajardo - AFAF

| ADR | Decision | HU / rama | Repositorio | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- |
| ADR-012 | OpenAPI / Swagger | HU-086 / `feature/HU-086-AFAF-openapi-documentation` | RematePos-Backend / RematePos-api | Requiere documentacion OpenAPI consumible por frontend y QA. | Pendiente |
| ADR-013 | Frontend por modulos/features | HU-050 / `feature/HU-050-AFAF-frontend-feature-structure` | RematePos-Frontend | Frontend organizado por features como sales, billing, inventory, customers; HU-30 y HU-35 consumen esta estructura desde sus flujos funcionales. | En implementacion |
| ADR-014 | Componentes compartidos | HU-051 / `feature/HU-051-AFAF-shared-components-library` | RematePos-Frontend | Requiere extraer controles comunes para botones, formularios, tablas y estados. | Pendiente |
| ADR-015 | JWT y guards | HU-073, HU-074, HU-075 / `feature/HU-073-AFAF-frontend-visual-security` | RematePos-Frontend / RematePos-api | Seguridad visual, persistencia de sesion y guards estan planificados. | Planeado |
| ADR-016 | Estado frontend por feature | HU-052 / `feature/HU-052-AFAF-feature-state-management` | RematePos-Frontend | Requiere formalizar estado de carrito, factura, sesion y productos por feature. | Pendiente |

### QA - Juan Sebastián Murcia Vargas - JSMV

| ADR | Decision | HU / rama | Repositorio | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- |
| ADR-011 | Configuracion externa por ambiente | HU-056, HU-082 / `feature/HU-82-CAVY-environment-strategy` | RematePos-Backend / RematePos-api | Variables por ambiente en frontend, gateway y compose estan identificadas. | En implementacion |
| ADR-017 | Logging estructurado y correlation ID | HU-087 / `feature/HU-087-JSMV-structured-logging-correlation-id` | RematePos-Backend / RematePos-api | Requiere trazabilidad entre Gateway, purchase, inventory e invoice. | Pendiente |
| ADR-018 | Docker Compose local | HU-057, HU-083 / `feature/HU-083-CAVY-rematepos-docker-compose` | RematePos-Backend / RematePos-api / RematePos-bd | DEV/QA/main ya tienen contenedores identificados; falta estandarizacion final. | En implementacion |
| ADR-019 | Pipeline CI | HU-058, HU-079, HU-080 | Todos los repos | Hay workflow inicial; falta pipeline activo por repo y validacion QA. | Pendiente |
| ADR-020 | Cache para catalogo de productos | HU-088 / `feature/HU-088-JSMV-product-catalog-cache` | RematePos-Backend | Requiere medir catalogo y definir estrategia cache invalidation. | Pendiente |

## ADRs pendientes y HUs propuestas

| ADR | Motivo de pendiente | HU propuesta |
| --- | --- | --- |
| ADR-008 | Los filtros dinamicos de productos deben evitar cargar listas completas y permitir busqueda escalable. | HU-055 |
| ADR-010 | Se necesita outbox para consistencia eventual entre pagos, inventario y facturacion cuando haya eventos. | HU-085 |
| ADR-012 | OpenAPI/Swagger debe documentar contratos para frontend, QA y Postman. | HU-086 |
| ADR-017 | Logging estructurado y correlation ID debe permitir seguir una venta entre Gateway y microservicios. | HU-087 |
| ADR-020 | Cache de catalogo debe mejorar rendimiento sin mostrar stock obsoleto. | HU-088 |

## Roadmap de implementacion recomendado

1. API Gateway.
2. Documentacion ADR aplicada.
3. Seguridad frontend/backend.
4. Devoluciones.
5. Ambientes DEV/QA/PROD.
6. Separacion de `purchase-microservice`.
7. `payment-service`.
8. `cash-register-service`.
9. `billing-service` con proveedor DIAN sandbox.
10. Docker Compose del ecosistema RematePOS.
11. QA integral.

## Reglas de cierre por ADR

Para marcar una ADR como aplicada, debe existir:

- HU asociada.
- Rama feature hija de `develop`.
- Commits convencionales en ingles.
- Repositorio correcto.
- Evidencia funcional o documental.
- PR hacia `develop`.
- Revision o aprobacion segun el flujo del equipo.

## Estado de este documento

| Campo | Valor |
| --- | --- |
| HU | HU-84 |
| Rama | `feature/HU-84-KSCH-document-applied-adrs` |
| Repositorio | RematePos |
| Tipo de cambio | Documentacion |
| Estado esperado | Ready to merge into `develop` |
