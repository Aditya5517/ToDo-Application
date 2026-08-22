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
    get_current_user,
    require_admin
)

from src.repositories.task_list_repository import (
    get_task_list_by_id,
    get_task_lists_by_project,
    get_task_list_members
)

from src.services.project_service import (
    can_access_project
)

from src.services.task_list_service import (
    create_task_list,
    can_access_task_list,
    update_task_list,
    add_task_list_member,
    remove_task_list_member
)

from src.schemas.task_list_schema import (
    TaskListCreate,
    TaskListUpdate,
    TaskListResponse,
    TaskListMemberCreate,
    TaskListMemberResponse
)


router = APIRouter(
    prefix="/task-lists",
    tags=["Task Lists"]
)


# =========================================================
# CREATE TASK LIST
# ADMIN ONLY
# =========================================================

@router.post(
    "",
    response_model=TaskListResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_task_list(
    task_list_data: TaskListCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    task_list, error = create_task_list(
        db=db,
        current_user=admin,
        project_id=task_list_data.project_id,
        name=task_list_data.name,
        description=task_list_data.description
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return task_list


# =========================================================
# LIST TASK LISTS OF PROJECT
# =========================================================

@router.get(
    "/project/{project_id}",
    response_model=list[TaskListResponse]
)
def project_task_lists(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    if not can_access_project(
        db,
        current_user,
        project_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Project access denied."
        )


    return get_task_lists_by_project(
        db,
        project_id
    )


# =========================================================
# GET TASK LIST
# =========================================================

@router.get(
    "/{task_list_id}",
    response_model=TaskListResponse
)
def get_task_list(
    task_list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    task_list = get_task_list_by_id(
        db,
        task_list_id
    )


    if task_list is None:

        raise HTTPException(
            status_code=404,
            detail="Task list not found."
        )


    if not can_access_task_list(
        db,
        current_user,
        task_list_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Task list access denied."
        )


    return task_list


# =========================================================
# UPDATE TASK LIST
# ADMIN ONLY
# =========================================================

@router.patch(
    "/{task_list_id}",
    response_model=TaskListResponse
)
def update_existing_task_list(
    task_list_id: int,
    task_list_data: TaskListUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    task_list, error = update_task_list(
        db,
        task_list_id,
        task_list_data
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return task_list


# =========================================================
# TASK LIST MEMBERS
# =========================================================

@router.get(
    "/{task_list_id}/members",
    response_model=list[
        TaskListMemberResponse
    ]
)
def task_list_members(
    task_list_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    if not can_access_task_list(
        db,
        current_user,
        task_list_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Task list access denied."
        )


    return get_task_list_members(
        db,
        task_list_id
    )


# =========================================================
# ADD MEMBER
# ADMIN ONLY
# =========================================================

@router.post(
    "/{task_list_id}/members",
    response_model=TaskListMemberResponse
)
def add_member(
    task_list_id: int,
    member_data: TaskListMemberCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    member, error = add_task_list_member(
        db=db,
        task_list_id=task_list_id,
        user_id=member_data.user_id,
        member_role=member_data.member_role
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return member


# =========================================================
# REMOVE MEMBER
# ADMIN ONLY
# =========================================================

@router.delete(
    "/{task_list_id}/members/{user_id}"
)
def remove_member(
    task_list_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    success, error = (
        remove_task_list_member(
            db,
            task_list_id,
            user_id
        )
    )


    if not success:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return {
        "message": (
            "Task list member "
            "removed successfully."
        )
    }