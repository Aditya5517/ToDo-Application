from datetime import (
    datetime,
    timezone
)

from sqlalchemy.orm import Session

from src.db_models.task import Task

from src.db_models.enums import (
    TaskStatus
)

from src.repositories.task_repository import (
    get_task_by_id
)

from src.repositories.task_list_repository import (
    get_task_list_by_id
)


def utc_now():

    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


def normalize_datetime(
    value: datetime | None
):

    if value is None:

        return None


    if value.tzinfo is not None:

        return (
            value
            .astimezone(timezone.utc)
            .replace(tzinfo=None)
        )


    return value


# =========================================================
# CREATE TASK
# =========================================================

def create_task(
    db: Session,
    current_user,
    task_data
):

    task_list = get_task_list_by_id(
        db,
        task_data.task_list_id
    )


    if task_list is None:

        return None, "Task list not found."


    if not task_list.is_active:

        return None, "Task list is inactive."


    start_date = normalize_datetime(
        task_data.start_date
    )

    due_date = normalize_datetime(
        task_data.due_date
    )


    if (
        start_date is not None
        and due_date < start_date
    ):

        return None, (
            "Due date cannot be "
            "before start date."
        )


    if task_data.parent_task_id is not None:

        parent_task = get_task_by_id(
            db,
            task_data.parent_task_id
        )


        if parent_task is None:

            return None, (
                "Parent task not found."
            )


        if (
            parent_task.task_list_id
            != task_data.task_list_id
        ):

            return None, (
                "Parent task must belong "
                "to the same task list."
            )


    completed_by = None
    completed_at = None


    if task_data.status == TaskStatus.completed:

        completed_by = current_user.id
        completed_at = utc_now()


    task = Task(
        task_list_id=task_data.task_list_id,
        parent_task_id=task_data.parent_task_id,
        title=task_data.title.strip(),
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        created_by=current_user.id,
        start_date=start_date,
        due_date=due_date,
        is_recurring=task_data.is_recurring,
        completed_by=completed_by,
        completed_at=completed_at,
        is_archived=False
    )


    db.add(task)

    db.commit()

    db.refresh(task)

    return task, None


# =========================================================
# UPDATE TASK
# =========================================================

def update_task(
    db: Session,
    current_user,
    task_id: int,
    task_data
):

    task = get_task_by_id(
        db,
        task_id
    )


    if task is None:

        return None, "Task not found."


    if task.is_archived:

        return None, (
            "Archived task cannot be updated."
        )


    updates = task_data.model_dump(
        exclude_unset=True
    )


    if "start_date" in updates:

        updates["start_date"] = (
            normalize_datetime(
                updates["start_date"]
            )
        )


    if "due_date" in updates:

        updates["due_date"] = (
            normalize_datetime(
                updates["due_date"]
            )
        )


    final_start_date = updates.get(
        "start_date",
        task.start_date
    )

    final_due_date = updates.get(
        "due_date",
        task.due_date
    )


    if (
        final_start_date is not None
        and final_due_date < final_start_date
    ):

        return None, (
            "Due date cannot be "
            "before start date."
        )


    if "status" in updates:

        new_status = updates["status"]


        if new_status == TaskStatus.completed:

            task.completed_by = (
                current_user.id
            )

            task.completed_at = utc_now()


        elif task.status == TaskStatus.completed:

            task.completed_by = None

            task.completed_at = None


    for key, value in updates.items():

        setattr(
            task,
            key,
            value
        )


    db.commit()

    db.refresh(task)

    return task, None


# =========================================================
# ARCHIVE TASK
# =========================================================

def archive_task(
    db: Session,
    current_user,
    task_id: int
):

    task = get_task_by_id(
        db,
        task_id
    )


    if task is None:

        return None, "Task not found."


    if task.is_archived:

        return None, (
            "Task is already archived."
        )


    task.is_archived = True

    task.archived_by = current_user.id

    task.archived_at = utc_now()


    db.commit()

    db.refresh(task)

    return task, None


# =========================================================
# RESTORE TASK
# =========================================================

def restore_task(
    db: Session,
    task_id: int
):

    task = get_task_by_id(
        db,
        task_id
    )


    if task is None:

        return None, "Task not found."


    if not task.is_archived:

        return None, (
            "Task is not archived."
        )


    task.is_archived = False

    task.archived_by = None

    task.archived_at = None


    db.commit()

    db.refresh(task)

    return task, None