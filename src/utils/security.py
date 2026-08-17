from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone


password_hash = PasswordHash.recommended()


SECRET_KEY = "change-this-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# =========================
# PASSWORD HASHING
# =========================

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

