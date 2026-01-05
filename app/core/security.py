"""Password hashing utilities.

Provides a small, well-tested interface used by domain models and services.
"""

from __future__ import annotations

import base64
import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from jose import JWTError, jwt

from app.core.config import settings

_ALGORITHM = 'pbkdf2_sha256'
_ITERATIONS = 120_000
_SALT_SIZE = 16  # bytes
TOKEN_ALGORITHM = 'HS256'


def hash_password(
    password: str, iterations: int = _ITERATIONS, salt: Optional[bytes] = None
) -> str:
    """Return a salted PBKDF2-SHA256 hashed password string.

    Format: "{algorithm}${iterations}${salt_b64}${dk_b64}"
    """
    if salt is None:
        salt = os.urandom(_SALT_SIZE)
    dk = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, iterations
    )
    salt_b64 = base64.b64encode(salt).decode('ascii')
    dk_b64 = base64.b64encode(dk).decode('ascii')
    return f'{_ALGORITHM}${iterations}${salt_b64}${dk_b64}'


def verify_password(stored: str, password: str) -> bool:
    """
    Verify the provided password against the stored hash.
    """
    try:
        algorithm, iterations_s, salt_b64, dk_b64 = stored.split('$')
    except ValueError:
        return False
    if algorithm != _ALGORITHM:
        return False
    try:
        iterations = int(iterations_s)
        salt = base64.b64decode(salt_b64)
        dk = base64.b64decode(dk_b64)
    except Exception:
        return False
    new_dk = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt, iterations
    )
    return secrets.compare_digest(new_dk, dk)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create a JWT access token including an expiry."""
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({'exp': expire})
    token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=TOKEN_ALGORITHM
    )
    return token


def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token.

    Returns the payload or raises ValueError on failure.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[TOKEN_ALGORITHM],
        )
        return payload
    except JWTError as exc:
        raise ValueError('Invalid token') from exc
