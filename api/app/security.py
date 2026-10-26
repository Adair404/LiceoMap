import time
import secrets
from threading import RLock
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from . import config
from .db import get_db, query_one

_bearer = HTTPBearer(auto_error=False)

# Hash de relleno para que el tiempo de respuesta no revele si el RUT existe
_DUMMY_HASH = bcrypt.hashpw(b"relleno", bcrypt.gensalt(10))


def verify_password(password: str, stored_hash: str | None) -> bool:
    target = stored_hash.encode() if stored_hash else _DUMMY_HASH
    try:
        encoded = password.encode()
        # bcrypt never silently treats two passwords with the same first 72 bytes as equal.
        if len(encoded) > 72:
            return False
        ok = bcrypt.checkpw(encoded, target)
    except ValueError:
        return False
    return ok and stored_hash is not None


def create_token(user_id: int, role: str, conn) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    session_id = secrets.token_hex(32)
    with conn.cursor() as cur:
        cur.execute('INSERT INTO auth_sessions (id_sesion,id_usuario,expira_en) VALUES (%s,%s,%s)',
                    (session_id, user_id, expires.replace(tzinfo=None)))
    return jwt.encode(
        {"sub": str(user_id), "rol": role, "exp": expires, "iat": datetime.now(timezone.utc),
         "jti": session_id, "iss": "liceomap", "aud": "liceomap-clients"},
        config.JWT_SECRET,
        algorithm="HS256",
    )


class LoginLimiter:
    """Limitador en memoria: bloquea tras demasiados fallos por IP y RUT."""

    def __init__(self):
        self._fails: dict[str, list[float]] = defaultdict(list)
        self._lock = RLock()

    def _recent(self, key: str) -> list[float]:
        cutoff = time.monotonic() - config.LOGIN_WINDOW_SECONDS
        self._fails[key] = [t for t in self._fails[key] if t > cutoff]
        return self._fails[key]

    def blocked(self, key: str) -> bool:
        with self._lock:
            return len(self._recent(key)) >= config.LOGIN_MAX_FAILS

    def register_fail(self, key: str) -> None:
        with self._lock:
            # Bound memory in this single-worker development limiter.
            if len(self._fails) > 10000:
                for stale in list(self._fails):
                    if not self._recent(stale):
                        self._fails.pop(stale, None)
                if len(self._fails) > 10000:
                    self._fails.pop(next(iter(self._fails)))
            self._recent(key).append(time.monotonic())

    def reset(self, key: str) -> None:
        with self._lock:
            self._fails.pop(key, None)


limiter = LoginLimiter()


def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    conn=Depends(get_db),
) -> dict:
    unauthorized = HTTPException(status.HTTP_401_UNAUTHORIZED, "Sesión inválida o expirada")
    if credentials is None:
        raise unauthorized
    try:
        payload = decode_token(credentials.credentials)
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise unauthorized
    session = query_one(conn, 'SELECT 1 AS ok FROM auth_sessions WHERE id_sesion=%s AND id_usuario=%s '
                       'AND revocada=FALSE AND expira_en>UTC_TIMESTAMP()', (payload['jti'], user_id))
    if session is None:
        raise unauthorized
    user = query_one(
        conn,
        "SELECT u.id_usuario, u.rut, u.nombre, u.apellido, r.nombre AS rol "
        "FROM usuarios u JOIN roles r ON r.id_rol = u.id_rol "
        "WHERE u.id_usuario = %s AND u.activo = TRUE",
        (user_id,),
    )
    if user is None:
        raise unauthorized
    return user


def decode_token(token: str):
    return jwt.decode(token, config.JWT_SECRET, algorithms=['HS256'], issuer='liceomap',
                      audience='liceomap-clients', options={'require': ['exp', 'sub', 'jti', 'iat']})


def require_roles(*roles: str):
    def checker(user: dict = Depends(current_user)) -> dict:
        if user["rol"] not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes permiso para esta acción")
        return user

    return checker
