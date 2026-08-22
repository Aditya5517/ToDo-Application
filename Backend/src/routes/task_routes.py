from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from src.database.connection import (
    get_db
)

from src.db_models.auth import User

from src.dependencies.auth_dependencies import (
    require_admin
)

from src.schemas.task_schema import (
    TaskCreate,
    TaskUpdate,
    TaskResponse
)

from src.repositories.task_repository import (
    get_task_by_id,
    get_active_tasks,
    get_archived_tasks,
    get_tasks_by_task_list
)

from src.services.task_service import (
    create_task,
    update_task,
    archive_task,
    restore_task
)


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# =========================================================
# CREATE TASK
# ADMIN ONLY
# =========================================================

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    task, error = create_task(
        db,
        admin,
        task_data
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return task


# =========================================================
# GET ACTIVE TASKS
# ADMIN ONLY FOR NOW
# =========================================================

@router.get(
    "",
    response_model=list[TaskResponse]
)
def get_tasks(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    return get_active_tasks(db)


# =========================================================
# GET ARCHIVED TASKS
# =========================================================

@router.get(
    "/archived",
    response_model=list[TaskResponse]
)
def archived_tasks(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    return get_archived_tasks(db)


# =========================================================
# GET TASKS BY TASK LIST
# =========================================================

@router.get(
    "/task-list/{task_list_id}",
    response_model=list[TaskResponse]
)
def task_list_tasks(
    task_list_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    return get_tasks_by_task_list(
        db,
        task_list_id
    )


# =========================================================
# GET TASK BY ID
# =========================================================

@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    task = get_task_by_id(
        db,
        task_id
    )


    if task is None:

        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )


    return task


# =========================================================
# UPDATE TASK
# ADMIN ONLY
# =========================================================

@router.patch(
    "/{task_id}",
    response_model=TaskResponse
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    task, error = update_task(
        db,
        admin,
        task_id,
        task_data
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return task


# =========================================================
# DELETE = SOFT ARCHIVE
# ADMIN ONLY
# =========================================================

@router.delete(
    "/{task_id}",
    response_model=TaskResponse
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    task, error = archive_task(
        db,
        admin,
        task_id
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return task


# =========================================================
# RESTORE ARCHIVED TASK
# =========================================================

@router.patch(
    "/{task_id}/restore",
    response_model=TaskResponse
)
def restore_archived_task(
    task_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    task, error = restore_task(
        db,
        task_id
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return task