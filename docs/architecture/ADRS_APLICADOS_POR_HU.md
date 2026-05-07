# ADRs Aplicados por Historia de Usuario

## Proposito del documento

Este documento evidencia como los Architectural Decision Records (ADRs) se aplican realmente en RematePOS mediante historias de usuario, ramas feature, commits convencionales, repositorios y evidencias funcionales.

La intencion no es solo listar decisiones arquitectonicas. Cada ADR debe poder trazarse asi:

```text
ADR -> HU -> rama feature -> commits -> repositorio -> evidencia funcional -> estado
```

Esta trazabilidad permite revisar si una decision ya fue aplicada, esta en implementacion o sigue pendiente para una fase posterior.

## Equipo e iniciales oficiales

| Integrante | Rol | Iniciales oficiales |
| --- | --- | --- |
| Carlos Andres Villamil Yusunguaira | Backend / DevOps | `CAVY` |
| Felipe Ardilla | Frontend | `AFAF` |
| Juan Sebastian Murcia | QA | `JSMV` |
| Kevin Santiago Cuesta | Product Owner | `KSCH` |

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
| Responsable | Carlos Andres Villamil Yusunguaira (`CAVY`) |
| Evidencia funcional | API Gateway standalone, rutas configuradas, CORS corregido, README actualizado y PR Draft hacia `develop`. |
| Commits | `feat(HU-053): add API Gateway Spring Boot project`; `feat(HU-053): configure backend service routes`; `fix(HU-053): resolve duplicated CORS configuration`; `chore(HU-053): configure gateway environment variables`; `docs(HU-053): update API Gateway README` |
| Estado | Aplicado |

## Matriz general ADR - HU - evidencia

| ADR | Decision arquitectonica | Responsable | HU relacionada | Rama feature | Repositorio | Commits relacionados | Evidencia funcional | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ADR-002 | API Gateway como entrada unica del frontend | CAVY | HU-053 | `feature/HU-053-CAVY-api-gateway` | RematePos-api | `feat`, `fix`, `chore`, `docs` de HU-053 | Gateway standalone en `:8080`, rutas a microservicios, CORS corregido | Aplicado |
| ADR-084 | Documentar ADRs aplicados por HU | KSCH | HU-84 | `feature/HU-84-KSCH-document-applied-adrs` | RematePos | `docs(HU-84): add applied ADR evidence documentation` | Documento de trazabilidad ADR-HU creado | En implementacion |

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
| ADR-010 | HU-054, HU-67, HU-69 | `feature/HU-085-CAVY-outbox-transaction-pattern` | RematePos-Backend | Pendiente |
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
| HU-72 | Estandarizar ramas y commits | ADR-084 | RematePos |
| HU-73 | Seguridad visual frontend | ADR-015 | RematePos-Frontend |
| HU-74 | Persistencia y expiracion de sesion | ADR-015, ADR-016 | RematePos-Frontend |
| HU-75 | Proteger endpoints privados con JWT | ADR-015 | RematePos-Backend / RematePos-api |
| HU-76 | Manifest y estabilidad frontend | ADR-013 | RematePos-Frontend |
| HU-77 | Fortalecer backend de devoluciones | ADR-006, ADR-007 | RematePos-Backend |
| HU-78 | Fortalecer frontend de devoluciones | ADR-013, ADR-016 | RematePos-Frontend |
| HU-79 | Plan de pruebas funcionales POS | ADR-019 | RematePos |
| HU-80 | Validar flujo completo venta-pago-factura | ADR-007, ADR-019 | RematePos |
| HU-81 | Criterios de aceptacion por HU | ADR-084 | RematePos |
| HU-82 | Ambientes DEV, QA y produccion | ADR-003, ADR-011, ADR-018 | RematePos-Backend / RematePos-bd |
| HU-83 | Docker Compose ecosistema RematePOS | ADR-018 | RematePos-Backend / RematePos-api / RematePos-bd |
| HU-84 | Documentar ADRs aplicados por HU | ADR-084 | RematePos |
