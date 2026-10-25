from datetime import datetime, timedelta, timezone
import json
import jwt
import pymysql
import pytest
from fastapi.testclient import TestClient

from app import config
from app.main import app
from app.security import verify_password
from conftest import ACCOUNTS, ROOT, cfg


@pytest.fixture
def client():
    return TestClient(app)


def headers(client, rut='20100002-5'):
    response = client.post('/auth/login', json={'rut': rut, 'password': ACCOUNTS[rut]})
    assert response.status_code == 200
    return {'Authorization': 'Bearer ' + response.json()['access_token']}


def admin_connection():
    return pymysql.connect(host='127.0.0.1', port=3308, user='root', password=cfg['MARIADB_ROOT_PASSWORD'],
                           database='liceomap_preoficial_test', autocommit=True)


def test_health_and_inactive(client):
    assert client.get('/health').json() == {'status': 'ok'}
    response = client.post('/auth/login', json={'rut': '20100008-4', 'password': ACCOUNTS['20100008-4']})
    assert response.status_code == 401
    assert 'password' not in response.text


@pytest.mark.parametrize('verb,path,body', [('get','/admin/anuncios',None),('get','/admin/cursos',None),
    ('post','/anuncios',{'titulo':'test','contenido':'test'}),('patch','/anuncios/1',{'titulo':'x'}),('delete','/anuncios/1',None)])
def test_all_admin_paths_reject_anonymous_and_student(client, verb, path, body):
    options = {'json': body} if body is not None else {}
    assert client.request(verb, path, **options).status_code == 401
    options['headers'] = headers(client, '20100006-8')
    assert client.request(verb, path, **options).status_code == 403


def test_real_crud_targeting_and_audit(client):
    admin = headers(client)
    first = headers(client, '20100006-8')
    second = headers(client, '20100007-6')
    ids = []
    for course in (None, '1F', '2A'):
        result = client.post('/anuncios', headers=admin,
                             json={'titulo':'pytest sincronización', 'contenido':'<script>texto inerte</script>', 'id_curso':course})
        assert result.status_code == 201, result.text
        assert result.json()['fecha_publicacion'].endswith('+00:00')
        ids.append(result.json()['id_anuncio'])
    visible1 = {a['id_anuncio'] for a in client.get('/anuncios', headers=first).json()}
    visible2 = {a['id_anuncio'] for a in client.get('/anuncios', headers=second).json()}
    assert ids[0] in visible1 & visible2
    assert ids[1] in visible1 and ids[1] not in visible2
    assert ids[2] in visible2 and ids[2] not in visible1
    aid = ids[1]
    response = client.patch(f'/anuncios/{aid}', headers=admin, json={'titulo':'Editado', 'id_curso':None})
    assert response.status_code == 200 and response.json()['titulo'] == 'Editado'
    assert aid in {a['id_anuncio'] for a in client.get('/anuncios', headers=second).json()}
    assert client.delete(f'/anuncios/{aid}', headers=admin).status_code == 200
    assert client.delete(f'/anuncios/{aid}', headers=admin).status_code == 200
    assert aid not in {a['id_anuncio'] for a in client.get('/anuncios', headers=first).json()}
    withdrawn = client.get('/admin/anuncios?estado=retirados', headers=admin).json()
    assert aid in {a['id_anuncio'] for a in withdrawn}
    history = client.get(f'/admin/anuncios/{aid}/historial', headers=admin).json()
    assert [h['accion'] for h in history] == ['CREAR', 'EDITAR', 'RETIRAR']
    assert json.loads(history[1]['datos'])['antes']['titulo'] == 'pytest sincronización'
    assert client.patch(f'/anuncios/{aid}', headers=admin, json={'titulo':'x'}).status_code == 409


@pytest.mark.parametrize('body',[{}, {'titulo':None}, {'titulo':'  '}, {'contenido':' '},
    {'publicado':True}, {'id_curso':''}, {'prioridad':'OTRA'}, {'titulo':'x'*151}])
def test_patch_validation(client, body):
    assert client.patch('/anuncios/1', headers=headers(client), json=body).status_code == 422


def test_recipient_errors_and_parametrization(client):
    admin = headers(client)
    for course in ['XXX', "1F' OR 1=1"]:
        response = client.post('/anuncios', headers=admin, json={'titulo':'a','contenido':'b','id_curso':course})
        assert response.status_code in (404,422)
    assert client.patch('/anuncios/999999', headers=admin, json={'titulo':'a'}).status_code == 404
    assert client.delete('/anuncios/999999', headers=admin).status_code == 404


def test_logout_expiry_and_revocation(client):
    auth = headers(client)
    assert client.get('/me', headers=auth).status_code == 200
    token = auth['Authorization'][7:]
    claims = jwt.decode(token, config.JWT_SECRET, algorithms=['HS256'], audience='liceomap-clients')
    claims['exp'] = datetime.now(timezone.utc) - timedelta(seconds=1)
    expired = jwt.encode(claims, config.JWT_SECRET, algorithm='HS256')
    assert client.get('/me', headers={'Authorization':'Bearer '+expired}).status_code == 401
    assert client.post('/auth/logout', headers=auth).status_code == 204
    assert client.get('/me', headers=auth).status_code == 401


def test_user_disabled_during_session(client):
    auth = headers(client, '20100007-6')
    with admin_connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("UPDATE usuarios SET activo=FALSE WHERE rut='20100007-6'")
                assert client.get('/me', headers=auth).status_code == 401
            finally:
                cur.execute("UPDATE usuarios SET activo=TRUE WHERE rut='20100007-6'")


def test_no_password_echo_or_bcrypt_truncation(client):
    secret = 'private-'*100
    response = client.post('/auth/login', json={'rut':'20100006-8','password':secret})
    assert response.status_code == 422 and secret not in response.text
    import bcrypt
    hashed = bcrypt.hashpw(b'a'*72, bcrypt.gensalt(4)).decode()
    assert verify_password('a'*72, hashed)
    assert not verify_password('a'*72+'b', hashed)


def test_cors(client):
    for origin in ['http://localhost:5500','http://127.0.0.1:5500']:
        response = client.options('/anuncios/1', headers={'Origin':origin,'Access-Control-Request-Method':'PATCH',
                                                        'Access-Control-Request-Headers':'authorization,content-type'})
        assert response.status_code == 200
        assert response.headers['access-control-allow-origin'] == origin
    assert client.options('/anuncios', headers={'Origin':'https://untrusted.example',
                                              'Access-Control-Request-Method':'POST'}).status_code == 400


def test_app_minimum_privileges():
    with pymysql.connect(host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER,
                         password=config.DB_PASSWORD, database=config.DB_NAME) as conn:
        with conn.cursor() as cur:
            for sql in ['DELETE FROM anuncios WHERE id_anuncio=-1',
                        'UPDATE usuarios SET activo=TRUE WHERE id_usuario=-1',
                        'DELETE FROM anuncios_historial WHERE id_historial=-1',
                        'UPDATE anuncios_historial SET accion=\'RETIRAR\' WHERE id_historial=-1']:
                with pytest.raises(pymysql.MySQLError):
                    cur.execute(sql)
