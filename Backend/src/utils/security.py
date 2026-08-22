import hashlib
import uuid

import jwt

from datetime import (
    datetime,
    timedelta,
    timezone
)

from pwdlib import PasswordHash

from src.config.settings import settings


password_hash = PasswordHash.recommended()


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password: str) -> str:

    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )


# =========================================================
# ACCESS TOKEN
# =========================================================

def create_access_token(
    user_id: int
) -> str:

    now = datetime.now(
        timezone.utc
    )

    expires_at = now + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": str(user_id),
        "type": "access",
        "iat": now,
        "exp": expires_at
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


# =========================================================
# REFRESH TOKEN
# =========================================================

def create_refresh_token(
    user_id: int
):

    now = datetime.now(
        timezone.utc
    )

    expires_at = now + timedelta(
        days=settings.refresh_token_expire_days
    )

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "jti": str(uuid.uuid4()),
        "iat": now,
        "exp": expires_at
    }

    token = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

    # Our PostgreSQL column uses TIMESTAMP
    # without timezone, while the DB itself
    # has been configured to UTC.
    db_expires_at = expires_at.replace(
        tzinfo=None
    )

    return token, db_expires_at


# =========================================================
# DECODE JWT
# =========================================================

def decode_token(
    token: str
) -> dict:

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[
            settings.jwt_algorithm
        ]
    )


# =========================================================
# HASH REFRESH TOKEN
# =========================================================

def hash_token(
    token: str
) -> str:

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()