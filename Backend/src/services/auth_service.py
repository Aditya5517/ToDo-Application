import secrets
import jwt

from datetime import (
    datetime,
    timedelta,
    timezone
)

from sqlalchemy.orm import Session

from src.repositories.user_repository import (
    get_user_by_email,
    get_user_by_id
)

from src.repositories.session_repository import (
    create_user_session,
    get_active_session,
    revoke_session,
    revoke_all_user_sessions
)

from src.repositories.auth_token_repository import (
    create_email_verification_record,
    get_valid_email_verification_token,
    create_password_reset_record,
    get_valid_password_reset_token,
    mark_all_reset_tokens_used
)

from src.utils.logs import logger

from src.utils.security import (
    verify_password,
    hash_password,
    hash_token,
    create_access_token,
    create_refresh_token,
    decode_token
)


def utc_now():

    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


# =========================================================
# AUTHENTICATE USER
# =========================================================

def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(
        db,
        email
    )

    if user is None:

        return None, "invalid"


    if not verify_password(
        password,
        user.password_hash
    ):

        return None, "invalid"


    if not user.is_active:

        return None, "inactive"


    if not user.is_email_verified:

        return None, "unverified"


    user.last_login_at = utc_now()

    db.commit()
    db.refresh(user)

    logger.info(
        f"User authenticated | "
        f"ID={user.id}"
    )

    return user, None


# =========================================================
# LOGIN TOKENS
# =========================================================

def create_login_tokens(
    db: Session,
    user
):

    access_token = create_access_token(
        user.id
    )

    refresh_token, expires_at = (
        create_refresh_token(
            user.id
        )
    )

    create_user_session(
        db=db,
        user_id=user.id,
        refresh_token=refresh_token,
        expires_at=expires_at
    )

    return (
        access_token,
        refresh_token
    )


# =========================================================
# REFRESH ACCESS TOKEN
# =========================================================

def refresh_access_token(
    db: Session,
    refresh_token: str
):

    try:

        payload = decode_token(
            refresh_token
        )

    except jwt.InvalidTokenError:

        return None


    if payload.get("type") != "refresh":

        return None


    session = get_active_session(
        db,
        refresh_token
    )

    if session is None:

        return None


    try:

        user_id = int(
            payload.get("sub")
        )

    except (TypeError, ValueError):

        return None


    user = get_user_by_id(
        db,
        user_id
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    if not user.is_email_verified:
        return None


    return create_access_token(
        user.id
    )


# =========================================================
# EMAIL VERIFICATION
# =========================================================

def generate_email_verification_token(
    db: Session,
    user_id: int
):

    raw_token = secrets.token_urlsafe(
        32
    )

    expires_at = utc_now() + timedelta(
        hours=24
    )

    create_email_verification_record(
        db=db,
        user_id=user_id,
        token_hash=hash_token(
            raw_token
        ),
        expires_at=expires_at
    )

    return raw_token


def verify_email(
    db: Session,
    raw_token: str
):

    token = (
        get_valid_email_verification_token(
            db,
            hash_token(raw_token)
        )
    )

    if token is None:
        return False


    user = get_user_by_id(
        db,
        token.user_id
    )

    if user is None:
        return False


    user.is_email_verified = True

    token.verified_at = utc_now()

    db.commit()

    return True


# =========================================================
# PASSWORD RESET
# =========================================================

def create_password_reset_token(
    db: Session,
    email: str
):

    user = get_user_by_email(
        db,
        email
    )

    if user is None:

        return None


    raw_token = secrets.token_urlsafe(
        32
    )

    expires_at = utc_now() + timedelta(
        minutes=30
    )

    create_password_reset_record(
        db=db,
        user_id=user.id,
        token_hash=hash_token(
            raw_token
        ),
        expires_at=expires_at
    )

    return raw_token


def reset_password(
    db: Session,
    raw_token: str,
    new_password: str
):

    token = (
        get_valid_password_reset_token(
            db,
            hash_token(raw_token)
        )
    )

    if token is None:

        return False


    user = get_user_by_id(
        db,
        token.user_id
    )

    if user is None:

        return False


    user.password_hash = hash_password(
        new_password
    )

    mark_all_reset_tokens_used(
        db,
        user.id
    )

    revoke_all_user_sessions(
        db,
        user.id
    )

    db.commit()

    logger.info(
        f"Password reset | user_id={user.id}"
    )

    return True


# =========================================================
# LOGOUT
# =========================================================

def logout_user(
    db: Session,
    refresh_token: str
):

    return revoke_session(
        db,
        refresh_token
    )


# =========================================================
# DEACTIVATE ACCOUNT
# =========================================================

def deactivate_account(
    db: Session,
    user,
    password: str
):

    if not verify_password(
        password,
        user.password_hash
    ):

        return False


    user.is_active = False

    user.deactivated_at = utc_now()

    revoke_all_user_sessions(
        db,
        user.id
    )

    db.commit()

    return True


# =========================================================
# REACTIVATE ACCOUNT
# =========================================================

def reactivate_account(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(
        db,
        email
    )

    if user is None:

        return None, "invalid"


    if not verify_password(
        password,
        user.password_hash
    ):

        return None, "invalid"


    if user.is_active:

        return user, "already_active"


    user.is_active = True

    user.reactivated_at = utc_now()

    db.commit()

    return user, None