"""Announcements share one authorization boundary and transactional audit trail."""
from contextlib import contextmanager
import json

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .db import get_db, query, query_one
from .security import current_user, require_roles

router = APIRouter()
publishers = require_roles('dev', 'utp', 'inspectoria')


class AnnouncementCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    titulo: str = Field(min_length=1, max_length=150)
    contenido: str = Field(min_length=1, max_length=5000)
    prioridad: str = Field(default='INFORMATIVO', pattern='^(INFORMATIVO|URGENTE|RECORDATORIO)$')
    id_curso: str | None = Field(default=None, min_length=1, max_length=10)


class AnnouncementPatch(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    titulo: str | None = Field(default=None, min_length=1, max_length=150)
    contenido: str | None = Field(default=None, min_length=1, max_length=5000)
    prioridad: str | None = Field(default=None, pattern='^(INFORMATIVO|URGENTE|RECORDATORIO)$')
    id_curso: str | None = Field(default=None, min_length=1, max_length=10)

    @field_validator('titulo', 'contenido', 'prioridad')
    @classmethod
    def non_null(cls, value):
        if value is None:
            raise ValueError('El campo no puede ser nulo')
        return value

    @model_validator(mode='after')
    def non_empty(self):
        if not self.model_fields_set:
            raise ValueError('No hay cambios')
        return self


SELECT = ('SELECT a.id_anuncio,a.id_curso,a.titulo,a.contenido,a.prioridad,a.publicado,'
          'a.fecha_publicacion,a.actualizado_en,CONCAT(u.nombre,\' \',u.apellido) AS autor '
          'FROM anuncios a JOIN usuarios u ON u.id_usuario=a.id_autor ')


def validate_course(conn, course):
    if course is not None and query_one(conn, 'SELECT 1 AS ok FROM cursos WHERE id_curso=%s AND activo=TRUE', (course,)) is None:
        raise HTTPException(404, 'Curso no encontrado o inactivo')


@contextmanager
def transaction(conn):
    conn.begin()
    try:
        yield
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def snapshot(conn, announcement_id, lock=False):
    item = query_one(conn, SELECT + 'WHERE a.id_anuncio=%s' + (' FOR UPDATE' if lock else ''), (announcement_id,))
    if item is None:
        raise HTTPException(404, 'Anuncio no encontrado')
    return item


def audit(conn, aid, uid, action, before, after):
    with conn.cursor() as cur:
        cur.execute('INSERT INTO anuncios_historial (id_anuncio,id_actor,accion,datos) VALUES (%s,%s,%s,%s)',
                    (aid, uid, action, json.dumps({'antes': before, 'despues': after}, ensure_ascii=False)))


@router.get('/anuncios')
def list_announcements(user=Depends(require_roles('alumno','profesor','dev','utp','inspectoria')), conn=Depends(get_db)):
    sql = SELECT + 'WHERE a.publicado=TRUE'
    params = ()
    if user['rol'] == 'alumno':
        sql += (' AND (a.id_curso IS NULL OR a.id_curso IN '
                '(SELECT ca.id_curso FROM curso_alumno ca JOIN cursos c ON c.id_curso=ca.id_curso '
                'WHERE ca.id_alumno=%s AND c.activo=TRUE))')
        params = (user['id_usuario'],)
    return query(conn, sql + ' ORDER BY a.fecha_publicacion DESC,a.id_anuncio DESC LIMIT 500', params)


@router.get('/admin/cursos')
def admin_courses(user=Depends(publishers), conn=Depends(get_db)):
    return query(conn, 'SELECT id_curso,nombre FROM cursos WHERE activo=TRUE ORDER BY nombre')


@router.get('/admin/anuncios')
def admin_announcements(estado: str = Query(default='todos', pattern='^(todos|publicados|retirados)$'),
                        destinatario: str | None = Query(default=None, min_length=1, max_length=10),
                        user=Depends(publishers), conn=Depends(get_db)):
    sql = SELECT + 'WHERE 1=1'
    params = []
    if estado != 'todos':
        sql += ' AND a.publicado=%s'
        params.append(estado == 'publicados')
    if destinatario == 'global':
        sql += ' AND a.id_curso IS NULL'
    elif destinatario:
        sql += ' AND a.id_curso=%s'
        params.append(destinatario)
    return query(conn, sql + ' ORDER BY a.fecha_publicacion DESC,a.id_anuncio DESC LIMIT 500', tuple(params))


@router.get('/admin/anuncios/{aid}/historial')
def history(aid: int, user=Depends(publishers), conn=Depends(get_db)):
    snapshot(conn, aid)
    return query(conn, 'SELECT id_historial,id_actor,accion,datos,creado_en FROM anuncios_historial '
                 'WHERE id_anuncio=%s ORDER BY id_historial', (aid,))


@router.post('/anuncios', status_code=201)
def create_announcement(payload: AnnouncementCreate, user=Depends(publishers), conn=Depends(get_db)):
    with transaction(conn):
        validate_course(conn, payload.id_curso)
        with conn.cursor() as cur:
            cur.execute('INSERT INTO anuncios (id_curso,id_autor,titulo,contenido,prioridad) VALUES (%s,%s,%s,%s,%s)',
                        (payload.id_curso, user['id_usuario'], payload.titulo, payload.contenido, payload.prioridad))
            aid = cur.lastrowid
        item = snapshot(conn, aid)
        audit(conn, aid, user['id_usuario'], 'CREAR', None, item)
    return item


@router.patch('/anuncios/{aid}')
def update_announcement(aid: int, payload: AnnouncementPatch, user=Depends(publishers), conn=Depends(get_db)):
    fields = payload.model_dump(exclude_unset=True)
    with transaction(conn):
        before = snapshot(conn, aid, lock=True)
        if not before['publicado']:
            raise HTTPException(409, 'El anuncio está retirado')
        if 'id_curso' in fields:
            validate_course(conn, fields['id_curso'])
        # Field identifiers come exclusively from the validated model; all values are parameters.
        with conn.cursor() as cur:
            cur.execute('UPDATE anuncios SET ' + ','.join(f'{key}=%s' for key in fields) + ' WHERE id_anuncio=%s',
                        (*fields.values(), aid))
        item = snapshot(conn, aid)
        audit(conn, aid, user['id_usuario'], 'EDITAR', before, item)
    return item


@router.delete('/anuncios/{aid}')
def withdraw_announcement(aid: int, user=Depends(publishers), conn=Depends(get_db)):
    with transaction(conn):
        before = snapshot(conn, aid, lock=True)
        if before['publicado']:
            with conn.cursor() as cur:
                cur.execute('UPDATE anuncios SET publicado=FALSE WHERE id_anuncio=%s', (aid,))
            audit(conn, aid, user['id_usuario'], 'RETIRAR', before, snapshot(conn, aid))
    return {'id_anuncio': aid, 'publicado': False}
