import pymysql
import pytest
from fastapi.testclient import TestClient

from app import config
from app.main import app
from app.rut import check_digit, normalize_rut
from conftest import ACCOUNTS

USERS = {
    "dev": ("20100001-7", "Dev2026!"),
    "utp": ("20100002-5", "Utp2026!"),
    "inspectoria": ("20100003-3", "Insp2026!"),
    "profesor": ("20100004-1", "Prof2026!"),
    "alumno": ("20100006-8", "Alum2026!"),
}
USERS = {role: (rut, ACCOUNTS[rut]) for role, (rut, _) in USERS.items()}


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def login(client, rol):
    rut, password = USERS[rol]
    response = client.post("/auth/login", json={"rut": rut, "password": password})
    assert response.status_code == 200, response.text
    return response.json()


def auth(client, rol):
    data = login(client, rol)
    return {"Authorization": f"Bearer {data['access_token']}"}, data["usuario"]


def test_rut_helpers():
    assert normalize_rut("20.100.005-k") == "20100005-K"
    assert check_digit("20100001") == "7"
    assert normalize_rut("1-9") is None


@pytest.mark.parametrize("rol", list(USERS))
def test_login_each_role(client, rol):
    assert login(client, rol)["usuario"]["rol"] == rol


def test_login_with_formatted_rut(client):
    response = client.post("/auth/login", json={"rut": "20.100.006-8", "password": ACCOUNTS['20100006-8']})
    assert response.status_code == 200


def test_login_wrong_password_and_unknown_user_same_message(client):
    wrong = client.post("/auth/login", json={"rut": "20100006-8", "password": "mala"})
    unknown = client.post("/auth/login", json={"rut": "20100009-2", "password": "mala"})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_login_invalid_rut(client):
    assert client.post("/auth/login", json={"rut": "1-9", "password": "x"}).status_code == 422


def test_protected_requires_token(client):
    assert client.get("/me").status_code in (401, 403)
    assert client.get("/anuncios").status_code in (401, 403)


def test_public_map_data(client):
    zonas = client.get("/zonas").json()
    ids = {z["id_zona"] for z in zonas}
    assert "bloque_b" in ids
    detail = next(z for z in zonas if z["id_zona"] == "bloque_b")["detalle_svg"]
    assert {d["piso"] for d in detail} == {1, 2}
    assert client.get("/zonas/bloque_b").status_code == 200
    assert client.get("/zonas/no_existe").status_code == 404
    assert client.get("/espacios").status_code == 200
    assert len(client.get("/bloques-horarios").json()) == 12


def test_alumno_only_sees_own_course(client):
    headers, _ = auth(client, "alumno")
    assert client.get("/cursos/1F/horarios", headers=headers).status_code == 200
    assert client.get("/cursos/2A/horarios", headers=headers).status_code == 403


def test_profesor_only_sees_own_schedule(client):
    headers, user = auth(client, "profesor")
    assert client.get(f"/profesores/{user['id_usuario']}/horarios", headers=headers).status_code == 200
    assert client.get(f"/profesores/{user['id_usuario'] + 1}/horarios", headers=headers).status_code == 403


def test_announcement_permissions(client):
    body = {"titulo": "Prueba pytest", "contenido": "contenido"}
    for rol in ("alumno", "profesor"):
        headers, _ = auth(client, rol)
        assert client.post("/anuncios", json=body, headers=headers).status_code == 403
    headers, _ = auth(client, "utp")
    assert client.post("/anuncios", json=body, headers=headers).status_code == 201


def test_alumno_sees_global_announcements(client):
    headers, _ = auth(client, "alumno")
    assert client.get("/anuncios", headers=headers).status_code == 200


def test_app_user_cannot_run_ddl():
    conn = pymysql.connect(
        host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER,
        password=config.DB_PASSWORD, database=config.DB_NAME,
    )
    try:
        with conn.cursor() as cur:
            with pytest.raises(pymysql.err.OperationalError):
                cur.execute("CREATE TABLE pytest_denegada (id INT)")
            with pytest.raises(pymysql.err.OperationalError):
                cur.execute("DROP TABLE roles")
    finally:
        conn.close()


def test_login_rate_limit(client):
    status = [
        client.post("/auth/login", json={"rut": "20100008-4", "password": "mala"}).status_code
        for _ in range(7)
    ]
    assert status[0] == 401
    assert 429 in status


def test_seed_data_courses_have_30_students():
    conn = pymysql.connect(host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER,
                           password=config.DB_PASSWORD, database=config.DB_NAME)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id_curso, COUNT(*) FROM curso_alumno GROUP BY id_curso")
            counts = dict(cur.fetchall())
    finally:
        conn.close()
    assert all(counts[c] == 30 for c in ("1F", "1G", "2A", "2B"))


def test_alumno_of_generated_data_can_login_and_see_full_schedule(client):
    # 1G no existía en la migración 002; primer alumno del curso según docs/datos_prueba.md
    conn = pymysql.connect(host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER,
                           password=config.DB_PASSWORD, database=config.DB_NAME)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT u.rut FROM usuarios u JOIN curso_alumno ca ON ca.id_alumno = u.id_usuario "
                        "WHERE ca.id_curso = '1G' LIMIT 1")
            rut = cur.fetchone()[0]
    finally:
        conn.close()
    token = client.post("/auth/login", json={"rut": rut, "password": ACCOUNTS[rut]}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    assert len(client.get("/cursos/1G/horarios", headers=headers).json()) == 30
