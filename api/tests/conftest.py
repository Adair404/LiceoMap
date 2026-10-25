"""Hard isolation: these tests can only target the generated dedicated test DB."""
import json
import os
from pathlib import Path
import sys

import pytest
from dotenv import dotenv_values

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'api'))
cfg = dotenv_values(ROOT / '.local/database.env')
accounts_path = ROOT / '.local/liceomap_preoficial_test.accounts.json'
if not accounts_path.exists():
    raise RuntimeError('Inicializar la base dedicada test con scripts/local_db.py init --test')
os.environ.update(DB_HOST='127.0.0.1', DB_PORT='3308', DB_NAME='liceomap_preoficial_test',
                  DB_USER='liceomap_test', DB_PASSWORD=cfg['APP_PASSWORD'], JWT_SECRET=cfg['JWT_SECRET'])
ACCOUNTS = {a['rut']: a['password'] for a in json.loads(accounts_path.read_text())}


@pytest.fixture(autouse=True)
def isolate_limiter():
    from app.security import limiter
    limiter._fails.clear()
    yield
    limiter._fails.clear()
