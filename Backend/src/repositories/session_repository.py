from datetime import (
    datetime,
    timezone
)

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.db_models.auth import UserSession
from src.utils.security import hash_token


def utc_now():

    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


def create_user_session(
    db: Session,
    user_id: int,
    refresh_token: str,
    expires_at: datetime
):

    session = UserSession(
        user_id=user_id,
        refresh_token_hash=hash_token(
            refresh_token
        ),
        expires_at=expires_at
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_active_session(
    db: Session,
    refresh_token: str
):

    statement = select(
        UserSession
    ).where(
        UserSession.refresh_token_hash
        == hash_token(refresh_token),

        UserSession.revoked_at.is_(None),

        UserSession.expires_at
        > utc_now()
    )

    return db.scalar(statement)


def revoke_session(
    db: Session,
    refresh_token: str
):

    session = get_active_session(
        db,
        refresh_token
    )

    if session is None:
        return False

    session.revoked_at = utc_now()

    db.commit()

    return True


def revoke_all_user_sessions(
    db: Session,
    user_id: int
):

    db.execute(
        update(UserSession)
        .where(
            UserSession.user_id == user_id,
            UserSession.revoked_at.is_(None)
        )
        .values(
            revoked_at=utc_now()
        )
    )