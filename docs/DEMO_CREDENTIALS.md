# Demo Credentials

Estas credenciales son locales/demo y deben cambiarse en produccion.

No incluir aqui tokens de proveedores, JWT, `INTERNAL_SERVICE_TOKEN`, `BILLING_PROVIDER_TOKEN`, `BILLING_SETTINGS_ENCRYPTION_KEY` ni archivos `.env` reales.

| Rol | Usuario | Contrasena | Uso |
|---|---|---|---|
| Platform super admin | `platform.admin` | Pendiente de confirmar localmente | Crear/ver tenants y owners iniciales desde plataforma. |
| Business owner demo | `admin.demo` | Pendiente de confirmar localmente | Gestion de negocio demo, productos, usuarios, ventas y facturacion. |
| Cashier demo | `cashier.demo` | Pendiente de confirmar localmente | Flujo de venta POS con permisos limitados. |
| Owner Gran Remate | Pendiente de confirmar localmente | Pendiente de confirmar localmente | Tenant `Gran Remate` usado en smoke HU-184A. |

Notas:

- El backend identifica `admin.demo` y `cashier.demo` como usuarios demo sembrados cuando `AUTH_SEED_DEMO_USERS` esta activo.
- Las contrasenas demo se toman desde variables/archivo local ignorado y no deben imprimirse en repositorio.
- Para exposicion, confirmar las contrasenas localmente antes de entregar el enlace.

