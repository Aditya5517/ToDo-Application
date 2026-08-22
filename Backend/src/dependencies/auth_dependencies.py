import jwt

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)

from sqlalchemy.orm import Session

from src.database.connection import (
    get_db
)

from src.db_models.auth import User

from src.db_models.enums import (
    UserRole
)

from src.repositories.user_repository import (
    get_user_by_id
)

from src.utils.security import (
    decode_token
)


bearer_scheme = HTTPBearer(
    auto_error=False
)


# =========================================================
# GET CURRENT LOGGED-IN USER
# =========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials
    = Depends(bearer_scheme),

    db: Session = Depends(get_db)
) -> User:

    if credentials is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    token = credentials.credentials


    try:

        payload = decode_token(
            token
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token.",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


    if payload.get("type") != "access":

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token."
        )


    try:

        user_id = int(
            payload.get("sub")
        )

    except (TypeError, ValueError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload."
        )


    user = get_user_by_id(
        db,
        user_id
    )


    if user is None:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found."
        )


    if not user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive."
        )


    return user


# =========================================================
# REQUIRE ADMIN
# =========================================================

def require_admin(
    current_user: User
    = Depends(get_current_user)
) -> User:

    if current_user.role != UserRole.admin:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )


    return current_user