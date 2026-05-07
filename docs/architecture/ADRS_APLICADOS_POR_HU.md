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
