"""Dedicated local database lifecycle. Never prints credentials or runs on arbitrary DBs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / '.local'
sys.path.insert(0, str(ROOT / 'api'))


def settings():
    from dotenv import dotenv_values
    return dotenv_values(LOCAL / 'database.env')


def secrets_init():
    LOCAL.mkdir(exist_ok=True)
    path = LOCAL / 'database.env'
    if not path.exists():
        path.write_text(f'MARIADB_ROOT_PASSWORD={secrets.token_urlsafe(36)}\n'
                        f'APP_PASSWORD={secrets.token_urlsafe(36)}\n'
                        f'JWT_SECRET={secrets.token_urlsafe(48)}\n', encoding='utf-8')
    cfg = settings()
    docker_env = LOCAL / 'mariadb.env'
    if not docker_env.exists():
        docker_env.write_text(f'MARIADB_ROOT_PASSWORD={cfg["MARIADB_ROOT_PASSWORD"]}\n', encoding='utf-8')
    target = ROOT / 'api' / '.env'
    if not target.exists():
        target.write_text('DB_HOST=127.0.0.1\nDB_PORT=3308\nDB_NAME=liceomap_preoficial_dev\n'
                          f'DB_USER=liceomap_app\nDB_PASSWORD={cfg["APP_PASSWORD"]}\n'
                          f'JWT_SECRET={cfg["JWT_SECRET"]}\nJWT_EXPIRE_MINUTES=60\n'
                          'CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500\n', encoding='utf-8')
    print('Configuración local preparada; secretos omitidos.')


def connect(database=None):
    import pymysql
    return pymysql.connect(host='127.0.0.1', port=3308, user='root',
                           password=settings()['MARIADB_ROOT_PASSWORD'], database=database,
                           charset='utf8mb4', autocommit=True)


def execute_script(cur, script):
    # Sources contain no procedures/delimiters; comments are removed before splitting.
    script = re.sub(r'^\s*--.*$', '', script, flags=re.M)
    for statement in script.split(';'):
        if statement.strip():
            cur.execute(statement)


def migrate(conn):
    with conn.cursor() as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS schema_migrations '
                    '(version VARCHAR(100) PRIMARY KEY, sha256 CHAR(64) NOT NULL, '
                    'applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)')
        for path in sorted((ROOT / 'database' / 'preoficial_migrations').glob('*.sql')):
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            cur.execute('SELECT sha256 FROM schema_migrations WHERE version=%s', (path.name,))
            row = cur.fetchone()
            if row:
                if row[0] != digest:
                    raise RuntimeError('Migración aplicada modificada: ' + path.name)
                continue
            execute_script(cur, path.read_text(encoding='utf-8'))
            cur.execute('INSERT INTO schema_migrations(version,sha256) VALUES (%s,%s)', (path.name, digest))
            print('Migración aplicada:', path.name)
        cur.execute('SELECT DATABASE()')
        dbname = cur.fetchone()[0]
        user = 'liceomap_app' if dbname.endswith('_dev') else 'liceomap_test'
        for host in ('localhost', '%'):
            cur.execute(f"GRANT SELECT,INSERT,UPDATE ON `{dbname}`.auth_sessions TO '{user}'@'{host}'")


def bootstrap(database, finish=False):
    # Only these two names on this loopback-only dedicated server are permitted.
    if database not in ('liceomap_preoficial_dev', 'liceomap_preoficial_test'):
        raise RuntimeError('Base no autorizada')
    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT GET_LOCK('liceomap_bootstrap',10)")
            if cur.fetchone()[0] != 1:
                raise RuntimeError('Otra inicialización está en curso')
            cur.execute('SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=%s', (database,))
            count = cur.fetchone()[0]
            receipt = LOCAL / f'{database}.initializing'
            if finish and not receipt.exists():
                raise RuntimeError('No existe recibo de inicialización interrumpida')
            if count and not finish:
                raise RuntimeError('INICIALIZACIÓN RECHAZADA: existen tablas. Usar migrate; nunca reinicializar.')
            if not finish:
                receipt.write_text('Instancia nueva verificada vacía; finalización pendiente.', encoding='utf-8')
                cur.execute(f'CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
                conn.select_db(database)
                script = (ROOT / 'database' / 'database.sql').read_text(encoding='utf-8')
                # The upstream schema explicitly names colegio_db: keep execution inside our empty DB.
                script = re.sub(r'CREATE DATABASE IF NOT EXISTS colegio_db.*?;', '', script, flags=re.S)
                script = re.sub(r'USE colegio_db;', '', script)
                execute_script(cur, script)
            else:
                conn.select_db(database)
            # Replace every publicly documented password. Keep synthetic courses/schedules.
            import bcrypt
            cur.execute('SELECT id_usuario, rut FROM usuarios')
            users = cur.fetchall()
            accounts = []
            for uid, rut in users:
                password = secrets.token_urlsafe(18)
                cur.execute('UPDATE usuarios SET password_hash=%s WHERE id_usuario=%s',
                            (bcrypt.hashpw(password.encode(), bcrypt.gensalt(10)).decode(), uid))
                accounts.append({'rut': rut, 'password': password})
            # Development content must never look like a validated institutional alert.
            cur.execute("UPDATE anuncios SET publicado=FALSE")
            cur.execute("UPDATE usuarios SET activo=FALSE WHERE rut='20100008-4'")
            for user, dbname in [('liceomap_app', 'liceomap_preoficial_dev'),
                                 ('liceomap_test', 'liceomap_preoficial_test')]:
                if dbname != database:
                    continue
                for host in ('localhost', '%'):
                    cur.execute('CREATE USER IF NOT EXISTS %s@%s IDENTIFIED BY %s', (user, host, settings()['APP_PASSWORD']))
                    # No DELETE, DDL, GRANT, or broad INSERT on users.
                    for table in ('roles', 'usuarios', 'cursos', 'curso_alumno', 'horarios', 'materias',
                                  'espacios', 'zonas', 'zonas_svg_detalle', 'bloques_horarios'):
                        cur.execute(f"GRANT SELECT ON `{database}`.`{table}` TO '{user}'@'{host}'")
                    cur.execute(f"GRANT SELECT,INSERT,UPDATE ON `{database}`.anuncios TO '{user}'@'{host}'")
            (LOCAL / f'{database}.accounts.json').write_text(json.dumps(accounts, indent=2), encoding='utf-8')
        migrate(conn)
        with conn.cursor() as cur:
            user = 'liceomap_app' if database.endswith('_dev') else 'liceomap_test'
            for host in ('localhost', '%'):
                cur.execute(f"GRANT SELECT,INSERT ON `{database}`.anuncios_historial TO '{user}'@'{host}'")
        receipt.unlink()
        print('Base dedicada inicializada:', database, '; cuentas en .local (no se imprimen).')
    finally:
        conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['secrets', 'init', 'finish-seed', 'migrate'])
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    dbname = 'liceomap_preoficial_test' if args.test else 'liceomap_preoficial_dev'
    if args.action == 'secrets':
        secrets_init()
    elif args.action in ('init', 'finish-seed'):
        bootstrap(dbname, finish=args.action == 'finish-seed')
    else:
        connection = connect(dbname)
        try:
            migrate(connection)
        finally:
            connection.close()
