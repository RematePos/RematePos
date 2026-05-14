# HU-103 - Local Execution Evidence

## Purpose

This document records the complete local execution evidence for RematePOS under HU-103.

The goal is to preserve the real validation results for the local RematePOS environment, including database services, backend microservices, API Gateway, frontend routes, invoice lookup, checkout, and cash payment flow.

This evidence represents a local validated environment. It is not a production deployment.

## Validation Date

- Validation date and time: 2026-05-12 21:25:24 -05:00.
- Scope: local validation only.
- Code changes during validation: none.
- Git operations during validation: no commits, no push, no merge.

## Local Workspaces

| Component | Workspace / URL |
| --- | --- |
| Database | Local database workspace. |
| Backend | Local backend functional workspace. |
| Frontend | Local validated frontend workspace. |
| API Gateway | `http://localhost:8080` |
| Frontend URL | `http://localhost:3000` |

Personal local filesystem paths were intentionally redacted from this shared documentation.

## Components Validated

- Database DEV environment.
- Backend functional stack.
- API Gateway through port `8080`.
- Frontend through port `3000`.
- Billing, invoice copy, and returns frontend routes.
- Checkout and cash payment flow.
- Invoice generation and lookup.

## Database Status

Database validation command:

```powershell
docker compose -p pos-db-dev --env-file .\docker-compose\.env.dev -f .\docker-compose\docker-compose.yml ps
```

Validated database services:

| Service | Image | Status | Port |
| --- | --- | --- | --- |
| PostgreSQL | `postgres:15-alpine` | Up and healthy | `5433 -> 5432` |
| MongoDB | `mongo:7` | Up | `27017 -> 27017` |

Notes:

- PostgreSQL DEV was running and healthy.
- MongoDB DEV was running.
- Liquibase and Mongo migrations had been executed previously with successful output.
- Real `.env` files are local only and are not included in this documentation.

## Backend Status

Backend validation command:

```powershell
docker compose -p pos-dev --env-file .\infra\docker\env\.env.dev -f .\infra\docker\compose\docker-compose.yml -f .\infra\docker\compose\docker-compose.dev.yml ps -a
```

Validated backend services:

| Service | Port | Status |
| --- | ---: | --- |
| discovery-server | 8761 | Up and healthy |
| config-server | 8888 | Up and healthy |
| api-gateway | 8080 | Up and healthy |
| customer-microservice | 8091 | Up |
| product-microservice | 8092 | Up |
| cart-microservice | 8093 | Up |
| purchase-microservice | 8094 | Up |
| invoice-microservice | 8095 | Up |

## API Gateway Status

- API Gateway URL: `http://localhost:8080`.
- Gateway used during validation: API Gateway included in the backend Docker Compose stack.
- Status: active and healthy.
- Note: the separated `RematePos-api` repository also exists, but this HU-103 validation used the gateway running inside the backend Compose stack.

## Frontend Status

- Frontend URL: `http://localhost:3000`.
- Status: active.
- Source during validation: local validated frontend workspace.

Validated frontend routes:

| Route | HTTP status | Result |
| --- | ---: | --- |
| `http://localhost:3000` | 200 | React SPA loaded |
| `http://localhost:3000/billing` | 200 | Billing route served |
| `http://localhost:3000/billing/invoice-copy` | 200 | Invoice copy route served |
| `http://localhost:3000/billing/returns` | 200 | Returns route served |

Observation:

- The official frontend repository is recovering the validated billing views through HU-121.
- HU-121 remains a Draft PR until team review.

## API Gateway Endpoints Validated

| Method | Endpoint | HTTP status | Result |
| --- | --- | ---: | --- |
| GET | `/api/v1/products` | 200 | Products available |
| GET | `/api/v1/customers` | 200 | Customers available |
| GET | `/api/v1/invoices/recent?limit=8` | 200 | Recent invoices available |
| GET | `/api/v1/invoices/number/INV-20260513-22` | 200 | Invoice found |
| GET | `/api/v1/purchases/22` | 200 | Purchase found |
| GET | `/api/v1/purchases/invoice/INV-20260513-22` | 200 | Purchase found by invoice number |
| POST | `/api/v1/purchases/checkout` | 200 | Checkout completed |
| POST | `/api/v1/purchases/22/pay` | 200 | Cash payment registered |

## Checkout And Cash Payment Flow

Validated flow:

| Step | Endpoint | Result |
| --- | --- | --- |
| Create purchase | `POST /api/v1/purchases/checkout` | 200 |
| Register cash payment | `POST /api/v1/purchases/22/pay` | 200 |
| Query paid purchase | `GET /api/v1/purchases/22` | 200 |
| Query generated invoice | `GET /api/v1/invoices/number/INV-20260513-22` | 200 |
| Query purchase by invoice | `GET /api/v1/purchases/invoice/INV-20260513-22` | 200 |

## Validated Data

| Field | Value |
| --- | --- |
| invoiceNumber | `INV-20260513-22` |
| purchaseId | `22` |
| invoiceId | `21` |
| paymentStatus | `PAID` |
| paymentMethod | `CASH` |
| providerStatus | `CONFIRMED_BY_CASHIER` |
| total | `5950.00` |

These values are test validation data used to demonstrate the local functional flow.

## Observations

- The complete functional backend was validated locally before all functionality was available in `origin/develop`.
- The backend functional baseline is preserved in HU-120 as a Draft PR for academic and technical review.
- The frontend functional views are being recovered into the official frontend repository through HU-121 as a Draft PR.
- HU-061 remains open and unmerged.
- PR #14 for HU-061 remains open and must not be merged automatically as part of this evidence.
- PR #15 for HU-120 preserves the broader backend functional baseline.
- PR #18 for HU-121 recovers the billing, invoice copy, and returns frontend views.
- The local validation did not perform commits, push, merge, `git clean`, `reset --hard`, or code changes.

## Security And Privacy Notes

This evidence intentionally excludes:

- real `.env` files;
- passwords;
- tokens;
- credentials;
- full logs;
- dumps;
- backups;
- generated build output;
- personal local filesystem paths.

Only local URLs and validation identifiers required for technical traceability are included.

## Next Steps

1. Review PR #15 for the HU-120 backend functional baseline.
2. Review PR #18 for the HU-121 frontend recovery.
3. Keep PR #14 open until the team decides the correct merge order for HU-061.
4. Split the broad backend baseline into smaller user stories, including payment, cash movement, webhook, invoice generation, and returns flows.
5. Document responsible AI-assisted development usage, including what was validated manually and what was generated or organized with assistant support.
6. Document future data transformation and predictive model work separately, without mixing it with the local execution evidence.
7. Continue excluding real secrets, environment files, logs, dumps, backups, generated files, and heavy artifacts from Git.
