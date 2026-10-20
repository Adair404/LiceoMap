# API LiceoMap (FastAPI)

Backend en `api/` que conecta con MariaDB (`colegio_db`) usando el usuario restringido `liceomap_app` (solo SELECT/INSERT/UPDATE/DELETE, sin DDL).

## Puesta en marcha
```bash
cd api
python -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env        # completar DB_PASSWORD y JWT_SECRET
.venv/bin/uvicorn app.main:app --port 8000
.venv/bin/python -m pytest  # tests
```
Documentación interactiva: http://localhost:8000/docs · Cliente de prueba: http://localhost:8000/test

## Endpoints
| Método | Ruta | Acceso |
|---|---|---|
| GET | `/health` | público |
| POST | `/auth/login` | público (RUT + contraseña; límite de 5 fallos / 5 min) |
| GET | `/me` | autenticado |
| GET | `/zonas`, `/zonas/{id}`, `/espacios`, `/bloques-horarios` | público |
| GET | `/cursos/{id}/horarios` | alumno de ese curso; staff (dev, utp, inspectoria, profesor) |
| GET | `/profesores/{id}/horarios` | el propio profesor; dev, utp, inspectoria |
| GET | `/anuncios` | autenticado (alumno: globales + sus cursos) |
| POST | `/anuncios` | dev, utp, inspectoria |

## Usuarios de prueba (datos sintéticos)
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
