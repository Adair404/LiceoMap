import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Falta la variable de entorno {name} (ver api/.env.example)")
    return value


DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3308"))
DB_NAME = os.getenv("DB_NAME", "liceomap_preoficial_dev")
DB_USER = _required("DB_USER")
DB_PASSWORD = _required("DB_PASSWORD")
JWT_SECRET = _required("JWT_SECRET")
if len(JWT_SECRET) < 32 or JWT_SECRET.startswith('cambiar'):
    raise RuntimeError('JWT_SECRET debe ser aleatorio y tener al menos 32 caracteres')
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
if not 1 <= JWT_EXPIRE_MINUTES <= 480:
    raise RuntimeError('JWT_EXPIRE_MINUTES fuera de rango')
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500").split(",") if o.strip()]

LOGIN_MAX_FAILS = 5
LOGIN_WINDOW_SECONDS = 300
