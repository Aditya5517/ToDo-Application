from sqlalchemy import (
    func,
    select
)

from sqlalchemy.orm import Session

from src.db_models.project import (
    TaskList,
    TaskListMember
)


def get_task_list_by_id(
    db: Session,
    task_list_id: int
):

    return db.scalar(
        select(TaskList)
        .where(
            TaskList.id == task_list_id
        )
    )


def get_task_list_by_name(
    db: Session,
    project_id: int,
    name: str
):

    return db.scalar(
        select(TaskList)
        .where(
            TaskList.project_id == project_id,

            func.lower(TaskList.name)
            == name.strip().lower()
        )
    )


def get_task_lists_by_project(
    db: Session,
    project_id: int
):

    return db.scalars(
        select(TaskList)
        .where(
            TaskList.project_id == project_id
        )
        .order_by(TaskList.id)
    ).all()


def get_task_list_member(
    db: Session,
    task_list_id: int,
    user_id: int
):

    return db.scalar(
        select(TaskListMember)
        .where(
            TaskListMember.task_list_id
            == task_list_id,

            TaskListMember.user_id
            == user_id
        )
    )


def get_task_list_members(
    db: Session,
    task_list_id: int
):

    return db.scalars(
        select(TaskListMember)
        .where(
            TaskListMember.task_list_id
            == task_list_id
        )
        .order_by(TaskListMember.id)
    ).all()