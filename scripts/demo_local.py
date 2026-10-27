#!/usr/bin/env python3
"""Run the existing local demo without migrations, seeds or implicit SQL writes."""
import argparse
import json
import os
from pathlib import Path
import runpy
import secrets
import subprocess
import sys
import urllib.error
import urllib.request

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / '.local' / 'demo.env'
REQUIRED_TABLES = {'usuarios', 'roles', 'cursos', 'curso_alumno', 'horarios',
                   'anuncios', 'anuncios_historial', 'auth_sessions'}


def read_config(path):
    from dotenv import dotenv_values
    if not path.is_file():
        raise RuntimeError('Falta configuración privada. Ejecuta configure --from con tu archivo local existente.')
    cfg = {k: v for k, v in dotenv_values(path).items() if v is not None}
    if cfg.get('DB_HOST') not in ('localhost', '127.0.0.1'):
        raise RuntimeError('La demostración exige MariaDB en loopback.')
    for key in ('DB_NAME', 'DB_USER', 'DB_PASSWORD'):
        if not cfg.get(key):
            raise RuntimeError('Falta configuración de conexión; valores omitidos.')
    int(cfg.get('DB_PORT', '3306'))
    return cfg


def configure(source, destination):
    cfg = read_config(source)
    cfg['DB_PORT'] = cfg.get('DB_PORT', '3306')
    if len(cfg.get('JWT_SECRET', '')) < 32 or cfg.get('JWT_SECRET', '').startswith('cambiar'):
        cfg['JWT_SECRET'] = secrets.token_urlsafe(48)
    cfg['JWT_EXPIRE_MINUTES'] = cfg.get('JWT_EXPIRE_MINUTES', '60')
    cfg['CORS_ORIGINS'] = 'http://127.0.0.1:5500,http://localhost:5500'
    keys = ('DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD',
            'JWT_SECRET', 'JWT_EXPIRE_MINUTES', 'CORS_ORIGINS')
    for key in keys:
        value = cfg[key]
        if '\n' in value or '\r' in value or "'" in value:
            raise RuntimeError('Valor de configuración no compatible; no se imprimió su contenido.')
    destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    # Never overwrite an existing private configuration.
    if destination.exists():
        print('Configuración privada existente conservada; usa check-db para comprobarla.')
        return
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as output:
        for key in keys:
            value = cfg[key]
            output.write(f"{key}='{value}'\n")
    print('Configuración privada creada con permisos 600; secretos omitidos. MariaDB no se modificó.')


def check_database(cfg):
    import pymysql
    conn = pymysql.connect(host=cfg['DB_HOST'], port=int(cfg.get('DB_PORT', '3306')),
                           user=cfg['DB_USER'], password=cfg['DB_PASSWORD'], database=cfg['DB_NAME'],
                           charset='utf8mb4', connect_timeout=3, read_timeout=5,
                           autocommit=False)
    try:
        with conn.cursor() as cur:
            cur.execute('START TRANSACTION READ ONLY')
            cur.execute('SELECT 1')
            cur.execute('SHOW TABLES')
            tables = {row[0] for row in cur.fetchall()}
            missing = sorted(REQUIRED_TABLES - tables)
            print(json.dumps({'database': cfg['DB_NAME'], 'connection': 'ok',
                              'missing_tables': missing, 'writes_performed': False}, ensure_ascii=False))
            if 'schema_migrations' in tables:
                cur.execute('SELECT version FROM schema_migrations ORDER BY version')
                print('Migraciones registradas:', ', '.join(str(row[0]) for row in cur.fetchall()))
            cur.execute('SELECT r.nombre, COUNT(*) FROM usuarios u JOIN roles r ON r.id_rol=u.id_rol '
                        'WHERE u.activo=TRUE GROUP BY r.nombre')
            print('Cuentas activas por rol:', json.dumps(dict(cur.fetchall()), ensure_ascii=False))
            return not missing
    finally:
        conn.rollback()
        conn.close()


def check_http():
    success = True
    for label, url in [('API', 'http://127.0.0.1:8000/health'), ('Web', 'http://127.0.0.1:5500/')]:
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                ok = response.status == 200
                if label == 'API':
                    ok = ok and json.load(response).get('status') == 'ok'
            print(label + (': OK' if ok else ': respuesta inesperada'))
            success &= ok
        except (urllib.error.URLError, TimeoutError, ValueError):
            print(label + ': no disponible')
            success = False
    return success


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    sub = parser.add_subparsers(dest='action', required=True)
    setup = sub.add_parser('configure')
    setup.add_argument('--from', dest='source', type=Path, required=True)
    for action in ('check-db', 'check', 'api', 'web', 'usb'):
        sub.add_parser(action)
    args = parser.parse_args()
    if args.action == 'configure':
        configure(args.source, args.config)
        return 0
    if args.action == 'check':
        return 0 if check_http() else 1
    if args.action == 'web':
        runpy.run_path(str(ROOT / 'scripts/run_web.py'), run_name='__main__')
        return 0
    if args.action == 'usb':
        adb = Path.home() / 'Android/Sdk/platform-tools/adb'
        if not adb.is_file():
            raise RuntimeError('No se encontró adb en el SDK instalado.')
        return subprocess.run([str(adb), 'reverse', 'tcp:8000', 'tcp:8000'], check=False).returncode
    cfg = read_config(args.config)
    if args.action == 'check-db':
        return 0 if check_database(cfg) else 1
    if len(cfg.get('JWT_SECRET', '')) < 32:
        raise RuntimeError('JWT_SECRET debe tener al menos 32 caracteres; usar configure.')
    os.environ.update(cfg)
    sys.path.insert(0, str(ROOT / 'api'))
    import uvicorn
    uvicorn.run('app.main:app', host='127.0.0.1', port=8000, access_log=False, workers=1)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print('Servicio detenido.')
    except Exception as exc:
        # Drivers and configuration errors can embed connection details. Keep them private.
        code = exc.args[0] if exc.args and isinstance(exc.args[0], int) else None
        print('No se pudo completar la operación. Tipo:', type(exc).__name__,
              'código:', code if code is not None else 'no disponible', file=sys.stderr)
        raise SystemExit(1)
