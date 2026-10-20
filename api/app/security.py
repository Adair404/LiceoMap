import time
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
        ok = bcrypt.checkpw(password.encode()[:72], target)
    except ValueError:
        return False
    return ok and stored_hash is not None


def create_token(user_id: int, role: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    return jwt.encode(
        {"sub": str(user_id), "rol": role, "exp": expires},
        config.JWT_SECRET,
        algorithm="HS256",
    )


class LoginLimiter:
    """Limitador en memoria: bloquea tras demasiados fallos por IP y RUT."""

    def __init__(self):
        self._fails: dict[str, list[float]] = defaultdict(list)

    def _recent(self, key: str) -> list[float]:
        cutoff = time.monotonic() - config.LOGIN_WINDOW_SECONDS
        self._fails[key] = [t for t in self._fails[key] if t > cutoff]
        return self._fails[key]

    def blocked(self, key: str) -> bool:
        return len(self._recent(key)) >= config.LOGIN_MAX_FAILS

    def register_fail(self, key: str) -> None:
        self._recent(key).append(time.monotonic())

    def reset(self, key: str) -> None:
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
        payload = jwt.decode(credentials.credentials, config.JWT_SECRET, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
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


def require_roles(*roles: str):
    def checker(user: dict = Depends(current_user)) -> dict:
        if user["rol"] not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes permiso para esta acción")
        return user

    return checker
