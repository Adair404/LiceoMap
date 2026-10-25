from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, ConfigDict
import pymysql

from . import config
from .db import get_db, query, query_one
from .rut import normalize_rut
from .security import (
    create_token,
    current_user,
    limiter,
    require_roles,
    verify_password,
    decode_token,
)
from .announcements import router as announcements_router

app = FastAPI(title="LiceoMap API", version="0.1.0")
app.include_router(announcements_router)


@app.exception_handler(pymysql.MySQLError)
async def database_error(request, exc):
    return JSONResponse(status_code=503, content={'detail': 'Servicio de datos no disponible. Intenta nuevamente.'})


@app.exception_handler(RequestValidationError)
async def validation_error(request, exc):
    # Pydantic input/ctx can contain passwords, SQL payloads, or private messages.
    return JSONResponse(status_code=422, content={'detail': 'Datos inválidos. Revisa los campos enviados.'})

if config.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )

STAFF_ROLES = ("dev", "utp", "inspectoria", "profesor")
PUBLISHER_ROLES = ("dev", "utp", "inspectoria")


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra='forbid')
    rut: str = Field(min_length=1, max_length=16)
    password: str = Field(min_length=1, max_length=128)


@app.get("/health")
def health(conn=Depends(get_db)):
    query_one(conn, "SELECT 1 AS ok")
    return {"status": "ok"}


# ---------------------------------------------------------------- Autenticación
@app.post("/auth/login")
def login(payload: LoginRequest, request: Request, conn=Depends(get_db)):
    ip = request.client.host if request.client else 'desconocida'
    if limiter.blocked('ip:' + ip):
        raise HTTPException(429, 'Demasiados intentos. Espera unos minutos.')
    rut = normalize_rut(payload.rut)
    if rut is None:
        limiter.register_fail('ip:' + ip)
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "RUT inválido")

    ip_key = f"{request.client.host if request.client else 'desconocida'}|{rut}"
    if limiter.blocked(ip_key) or limiter.blocked(rut):
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, "Demasiados intentos. Espera unos minutos.")

    user = query_one(
        conn,
        "SELECT u.id_usuario, u.rut, u.nombre, u.apellido, u.password_hash, r.nombre AS rol "
        "FROM usuarios u JOIN roles r ON r.id_rol = u.id_rol "
        "WHERE u.rut = %s AND u.activo = TRUE",
        (rut,),
    )
    if not verify_password(payload.password, user["password_hash"] if user else None):
        limiter.register_fail(ip_key)
        limiter.register_fail(rut)
        limiter.register_fail('ip:' + ip)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "RUT o contraseña incorrectos")

    limiter.reset(ip_key)
    limiter.reset(rut)
    public = {k: user[k] for k in ("id_usuario", "rut", "nombre", "apellido", "rol")}
    return {"access_token": create_token(user["id_usuario"], user["rol"], conn), "token_type": "bearer", "usuario": public,
            'expires_in': config.JWT_EXPIRE_MINUTES * 60}


@app.post('/auth/logout', status_code=204)
def logout(user=Depends(current_user), credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()), conn=Depends(get_db)):
    payload = decode_token(credentials.credentials)
    with conn.cursor() as cur:
        cur.execute('UPDATE auth_sessions SET revocada=TRUE WHERE id_sesion=%s AND id_usuario=%s',
                    (payload['jti'], user['id_usuario']))


@app.get("/me")
def me(user: dict = Depends(current_user), conn=Depends(get_db)):
    courses = query(
        conn,
        "SELECT c.id_curso, c.nombre FROM curso_alumno ca JOIN cursos c ON c.id_curso = ca.id_curso "
        "WHERE ca.id_alumno = %s AND c.activo=TRUE",
        (user["id_usuario"],),
    )
    return {**user, "cursos": courses}


# ---------------------------------------------------------------- Mapa (lectura pública)
@app.get("/zonas")
def list_zones(conn=Depends(get_db)):
    zones = query(
        conn,
        "SELECT id_zona, nombre, tipo, id_svg, latitud, longitud FROM zonas WHERE activo = TRUE ORDER BY id_zona",
    )
    details = query(conn, "SELECT id_zona, piso, archivo_svg FROM zonas_svg_detalle ORDER BY id_zona, piso")
    by_zone: dict[str, list[dict]] = {}
    for item in details:
        by_zone.setdefault(item["id_zona"], []).append({"piso": item["piso"], "archivo_svg": item["archivo_svg"]})
    for zone in zones:
        zone["detalle_svg"] = by_zone.get(zone["id_zona"], [])
    return zones


@app.get("/zonas/{zone_id}")
def get_zone(zone_id: str, conn=Depends(get_db)):
    zone = next((z for z in list_zones(conn) if z["id_zona"] == zone_id), None)
    if zone is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Zona no encontrada")
    zone["espacios"] = query(
        conn,
        "SELECT id_espacio, nombre, tipo, piso, id_svg FROM espacios WHERE id_zona = %s AND activo = TRUE "
        "ORDER BY piso, id_espacio",
        (zone_id,),
    )
    return zone


@app.get("/espacios")
def list_spaces(
    zona: str | None = Query(default=None, max_length=40),
    tipo: str | None = Query(default=None, pattern="^(AULA|ADMINISTRACION|TALLER|DEPORTE|OTRO)$"),
    conn=Depends(get_db),
):
    sql = (
        "SELECT id_espacio, nombre, tipo, pabellon_bloque, id_zona, id_svg, piso "
        "FROM espacios WHERE activo = TRUE"
    )
    params: list = []
    if zona:
        sql += " AND id_zona = %s"
        params.append(zona)
    if tipo:
        sql += " AND tipo = %s"
        params.append(tipo)
    return query(conn, sql + " ORDER BY id_espacio", tuple(params))


@app.get("/bloques-horarios")
def list_blocks(conn=Depends(get_db)):
    return query(
        conn, "SELECT id_bloque, numero, nombre, tipo, hora_inicio, hora_fin FROM bloques_horarios ORDER BY numero"
    )


# ---------------------------------------------------------------- Horarios
_SCHEDULE_SQL = (
    "SELECT h.id_horario, h.id_curso, h.dia_semana, b.numero AS bloque, b.nombre AS bloque_nombre, "
    "h.hora_inicio, h.hora_fin, m.nombre AS materia, h.id_profesor, "
    "CONCAT(p.nombre, ' ', p.apellido) AS profesor, h.id_espacio, e.nombre AS espacio, e.id_zona, e.id_svg "
    "FROM horarios h "
    "JOIN materias m ON m.id_materia = h.id_materia "
    "JOIN usuarios p ON p.id_usuario = h.id_profesor "
    "JOIN espacios e ON e.id_espacio = h.id_espacio "
    "LEFT JOIN bloques_horarios b ON b.id_bloque = h.id_bloque "
)


@app.get("/cursos/{course_id}/horarios")
def course_schedule(course_id: str, user: dict = Depends(require_roles('alumno', *STAFF_ROLES)), conn=Depends(get_db)):
    if user["rol"] == "alumno":
        enrolled = query_one(
            conn,
            "SELECT 1 AS ok FROM curso_alumno ca JOIN cursos c ON c.id_curso=ca.id_curso "
            "WHERE ca.id_alumno = %s AND ca.id_curso = %s AND c.activo=TRUE",
            (user["id_usuario"], course_id),
        )
        if enrolled is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes ver el horario de tu curso")
    elif query_one(conn, "SELECT 1 AS ok FROM cursos WHERE id_curso = %s", (course_id,)) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Curso no encontrado")
    return query(conn, _SCHEDULE_SQL + "WHERE h.id_curso = %s ORDER BY h.dia_semana, h.hora_inicio", (course_id,))


@app.get("/profesores/{teacher_id}/horarios")
def teacher_schedule(
    teacher_id: int,
    user: dict = Depends(require_roles(*STAFF_ROLES)),
    conn=Depends(get_db),
):
    if user["rol"] == "profesor" and user["id_usuario"] != teacher_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes ver tu propio horario")
    return query(conn, _SCHEDULE_SQL + "WHERE h.id_profesor = %s ORDER BY h.dia_semana, h.hora_inicio", (teacher_id,))


