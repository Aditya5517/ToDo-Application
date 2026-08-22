from datetime import (
    datetime,
    timezone
)

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.db_models.auth import (
    EmailVerificationToken,
    PasswordResetToken
)


def utc_now():

    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


# =========================================================
# EMAIL VERIFICATION TOKEN
# =========================================================

def create_email_verification_record(
    db: Session,
    user_id: int,
    token_hash: str,
    expires_at: datetime
):

    token = EmailVerificationToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return token


def get_valid_email_verification_token(
    db: Session,
    token_hash: str
):

    statement = select(
        EmailVerificationToken
    ).where(
        EmailVerificationToken.token_hash == token_hash,
        EmailVerificationToken.verified_at.is_(None),
        EmailVerificationToken.expires_at > utc_now()
    )

    return db.scalar(statement)


# =========================================================
# PASSWORD RESET TOKEN
# =========================================================

def create_password_reset_record(
    db: Session,
    user_id: int,
    token_hash: str,
    expires_at: datetime
):

    token = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return token


def get_valid_password_reset_token(
    db: Session,
    token_hash: str
):

    statement = select(
        PasswordResetToken
    ).where(
        PasswordResetToken.token_hash == token_hash,
        PasswordResetToken.used_at.is_(None),
        PasswordResetToken.expires_at > utc_now()
    )

    return db.scalar(statement)


def mark_all_reset_tokens_used(
    db: Session,
    user_id: int
):

    db.execute(
        update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user_id,
            PasswordResetToken.used_at.is_(None)
        )
        .values(
            used_at=utc_now()
        )
    )