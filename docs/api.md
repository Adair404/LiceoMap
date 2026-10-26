# API LiceoMap (FastAPI)

Backend en `api/` que conecta con MariaDB mediante un usuario restringido, sin DDL.
La integración preoficial usa `127.0.0.1:3308`, base `liceomap_preoficial_dev` y
usuario `liceomap_app`. La base dedicada de pruebas es `liceomap_preoficial_test`.
`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASSWORD` permiten conservar una
instalación upstream configurada con `colegio_db` en 3306, siempre que su esquema
sea compatible. Consultar [PREOFICIAL_INTEGRACION.md](PREOFICIAL_INTEGRACION.md).

## Puesta en marcha
Desde la raíz del repositorio, en PowerShell:

```powershell
.\.venv\Scripts\python.exe scripts/run_api.py
```
El helper y Uvicorn cargan `api/.env`. Configurarlo a partir de `api/.env.example`
con credenciales locales privadas, o pasar variables
de entorno (tienen precedencia sobre el archivo). `JWT_SECRET` debe ser aleatorio,
tener al menos 32 caracteres y no ser el placeholder. La vigencia predeterminada
es 60 minutos; se admiten valores entre 1 y 480. `CORS_ORIGINS` permite los orígenes
web explícitos; por defecto localhost y 127.0.0.1 en 5500, con GET/POST/PATCH/DELETE.

No reinicializar bases existentes ni reejecutar las migraciones históricas 001–003.
Se conservan las migraciones preoficiales 004 (historial) y 005 (`auth_sessions`);
este documento no indica ejecutarlas automáticamente sobre una base existente.

Documentación interactiva: http://localhost:8000/docs · Cliente de prueba: http://localhost:8000/test

## Endpoints
| Método | Ruta | Acceso |
|---|---|---|
| GET | `/health` | público |
| POST | `/auth/login` | público (RUT + contraseña; límite de 5 fallos / 5 min) |
| POST | `/auth/logout` | autenticado; revoca la sesión y responde 204 |
| GET | `/me` | autenticado |
| GET | `/zonas`, `/zonas/{id}`, `/espacios`, `/bloques-horarios` | público |
| GET | `/cursos/{id}/horarios` | alumno de ese curso; staff (dev, utp, inspectoria, profesor) |
| GET | `/profesores/{id}/horarios` | el propio profesor; dev, utp, inspectoria |
| GET | `/anuncios` | autenticado (alumno: globales + sus cursos) |
| POST | `/anuncios` | dev, utp, inspectoria |
| PATCH | `/anuncios/{id}` | dev, utp, inspectoria; edición de publicados |
| DELETE | `/anuncios/{id}` | dev, utp, inspectoria; retirada lógica idempotente |
| GET | `/admin/cursos` | dev, utp, inspectoria; cursos activos |
| GET | `/admin/anuncios` | dev, utp, inspectoria; filtros `estado` y `destinatario` |
| GET | `/admin/anuncios/{id}/historial` | dev, utp, inspectoria |

El login devuelve `access_token`, `token_type`, `usuario` y `expires_in` en segundos.
Enviar `Authorization: Bearer <token>` en las peticiones protegidas. Cada JWT HS256
incluye `sub`, `jti`, `iat`, `exp`, emisor `liceomap` y audiencia `liceomap-clients`.
Cada petición comprueba la sesión no revocada/no expirada y el usuario activo con
su rol actual en BD. Logout invalida ese token para las peticiones posteriores.

El CRUD se registra una sola vez desde `api/app/announcements.py`; conserva los
campos originales y añade estado y actualización en UTC. Creación, edición y
retirada registran historial en la misma transacción. Los retirados desaparecen
del listado público, por lo que web y Android observan los cambios al actualizar.
Los errores de validación y BD tienen respuestas seguras sin eco de datos privados.

## Pruebas

`api/tests/conftest.py` obliga a usar la base dedicada de pruebas y las cuentas de
`.local/liceomap_preoficial_test.accounts.json`. La suite completa escribe anuncios,
sesiones y cambios temporales de usuarios. Ejecutarla solo en un entorno de prueba
autorizado; no ejecutarla si se requiere conservar intactas todas las bases existentes.

```powershell
.\.venv\Scripts\python.exe -m pytest api/tests -q
```

## Usuarios históricos de upstream (datos sintéticos)

Estas contraseñas pertenecen exclusivamente a los seeds históricos de upstream.
No son válidas en las bases locales integradas: sus contraseñas aleatorias se
consultan localmente en `.local/liceomap_preoficial_dev.accounts.json` o en el
archivo equivalente de test, nunca se copian a Git.
| RUT | Contraseña | Rol |
|---|---|---|
| 20100001-7 | Dev2026! | dev |
| 20100002-5 | Utp2026! | utp |
| 20100003-3 | Insp2026! | inspectoria |
| 20100004-1 | Prof2026! | profesor |
| 20100005-K | Prof2026! | profesor |
| 20100006-8 | Alum2026! | alumno (1F) |
| 20100007-6, 20100008-4 | Alum2026! | alumno (2A) |

Solo para desarrollo; cambiarlas antes de cualquier uso real. `api/.env` está en `.gitignore`.

La lista completa (120 alumnos en 1F, 1G, 2A y 2B, más el personal) está en [datos_prueba.md](datos_prueba.md). Se genera con `database/tools/generar_datos_prueba.py`.
