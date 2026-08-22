from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db_models.task import Task


def get_task_by_id(
    db: Session,
    task_id: int
):

    return db.scalar(
        select(Task)
        .where(
            Task.id == task_id
        )
    )


def get_active_tasks(
    db: Session
):

    return db.scalars(
        select(Task)
        .where(
            Task.is_archived.is_(False)
        )
        .order_by(Task.id)
    ).all()


def get_archived_tasks(
    db: Session
):

    return db.scalars(
        select(Task)
        .where(
            Task.is_archived.is_(True)
        )
        .order_by(Task.id)
    ).all()


def get_tasks_by_task_list(
    db: Session,
    task_list_id: int
):

    return db.scalars(
        select(Task)
        .where(
            Task.task_list_id
            == task_list_id,

            Task.is_archived.is_(False)
        )
        .order_by(Task.id)
    ).all()