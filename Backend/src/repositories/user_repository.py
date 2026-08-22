from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.db_models.auth import User


def get_user_by_email(
    db: Session,
    email: str
):

    statement = select(User).where(
        func.lower(User.email)
        == email.strip().lower()
    )

    return db.scalar(statement)


def get_user_by_id(
    db: Session,
    user_id: int
):

    statement = select(User).where(
        User.id == user_id
    )

    return db.scalar(statement)


def get_all_users(
    db: Session
):

    statement = (
        select(User)
        .order_by(User.id)
    )

    return db.scalars(
        statement
    ).all()


def add_user(
    db: Session,
    user: User
):

    db.add(user)

    db.commit()

    db.refresh(user)

    return user