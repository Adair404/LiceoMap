from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import config
from .db import get_db, query, query_one
from .rut import normalize_rut
from .security import (
    create_token,
    current_user,
    limiter,
    require_roles,
    verify_password,
)

app = FastAPI(title="LiceoMap API", version="0.1.0")

if config.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGINS,
        allow_methods=["GET", "POST"],
        allow_headers=["Authorization", "Content-Type"],
    )

STAFF_ROLES = ("dev", "utp", "inspectoria", "profesor")
PUBLISHER_ROLES = ("dev", "utp", "inspectoria")


class LoginRequest(BaseModel):
    rut: str = Field(max_length=16)
    password: str = Field(min_length=1, max_length=128)


class AnnouncementCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    contenido: str = Field(min_length=1, max_length=5000)
    prioridad: str = Field(default="INFORMATIVO", pattern="^(INFORMATIVO|URGENTE|RECORDATORIO)$")
    id_curso: str | None = Field(default=None, max_length=10)


@app.get("/health")
def health(conn=Depends(get_db)):
    query_one(conn, "SELECT 1 AS ok")
    return {"status": "ok"}


# ---------------------------------------------------------------- Autenticación
@app.post("/auth/login")
def login(payload: LoginRequest, request: Request, conn=Depends(get_db)):
    rut = normalize_rut(payload.rut)
    if rut is None:
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
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "RUT o contraseña incorrectos")

    limiter.reset(ip_key)
    limiter.reset(rut)
    public = {k: user[k] for k in ("id_usuario", "rut", "nombre", "apellido", "rol")}
    return {"access_token": create_token(user["id_usuario"], user["rol"]), "token_type": "bearer", "usuario": public}


@app.get("/me")
def me(user: dict = Depends(current_user), conn=Depends(get_db)):
    courses = query(
        conn,
        "SELECT c.id_curso, c.nombre FROM curso_alumno ca JOIN cursos c ON c.id_curso = ca.id_curso "
        "WHERE ca.id_alumno = %s",
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
def course_schedule(course_id: str, user: dict = Depends(current_user), conn=Depends(get_db)):
    if user["rol"] == "alumno":
        enrolled = query_one(
            conn,
            "SELECT 1 AS ok FROM curso_alumno WHERE id_alumno = %s AND id_curso = %s",
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


# ---------------------------------------------------------------- Anuncios
@app.get("/anuncios")
def list_announcements(user: dict = Depends(current_user), conn=Depends(get_db)):
    sql = (
        "SELECT a.id_anuncio, a.id_curso, a.titulo, a.contenido, a.prioridad, a.fecha_publicacion, "
        "CONCAT(u.nombre, ' ', u.apellido) AS autor "
        "FROM anuncios a JOIN usuarios u ON u.id_usuario = a.id_autor WHERE a.publicado = TRUE"
    )
    params: tuple = ()
    if user["rol"] == "alumno":
        sql += " AND (a.id_curso IS NULL OR a.id_curso IN (SELECT id_curso FROM curso_alumno WHERE id_alumno = %s))"
        params = (user["id_usuario"],)
    return query(conn, sql + " ORDER BY a.fecha_publicacion DESC, a.id_anuncio DESC", params)


@app.post("/anuncios", status_code=status.HTTP_201_CREATED)
def create_announcement(
    payload: AnnouncementCreate,
    user: dict = Depends(require_roles(*PUBLISHER_ROLES)),
    conn=Depends(get_db),
):
    if payload.id_curso is not None and (
        query_one(conn, "SELECT 1 AS ok FROM cursos WHERE id_curso = %s", (payload.id_curso,)) is None
    ):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Curso no encontrado")
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO anuncios (id_curso, id_autor, titulo, contenido, prioridad) VALUES (%s, %s, %s, %s, %s)",
            (payload.id_curso, user["id_usuario"], payload.titulo, payload.contenido, payload.prioridad),
        )
        return {"id_anuncio": cur.lastrowid}


_TEST_CLIENT = Path(__file__).resolve().parent.parent / "test_client"
if _TEST_CLIENT.is_dir():
    app.mount("/test", StaticFiles(directory=_TEST_CLIENT, html=True), name="test_client")
