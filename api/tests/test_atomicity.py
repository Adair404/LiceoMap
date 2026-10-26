from fastapi import HTTPException
from fastapi.testclient import TestClient
from app import announcements
from app.main import app
from test_preoficial import admin_connection, headers


def test_announcement_and_history_are_atomic(monkeypatch):
    client = TestClient(app)
    auth = headers(client)
    with admin_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM anuncios')
            before = cursor.fetchone()[0]
    def unavailable_audit(*_):
        raise HTTPException(503,'Servicio de datos no disponible')
    monkeypatch.setattr(announcements,'audit',unavailable_audit)
    result = client.post('/anuncios',headers=auth,json={'titulo':'Atomicidad pytest','contenido':'Debe revertirse'})
    assert result.status_code == 503
    with admin_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM anuncios')
            assert cursor.fetchone()[0] == before
