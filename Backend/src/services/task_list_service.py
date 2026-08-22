from sqlalchemy.orm import Session

from src.db_models.project import (
    TaskList,
    TaskListMember
)

from src.db_models.enums import (
    ProjectMemberRole,
    UserRole
)

from src.repositories.project_repository import (
    get_project_by_id,
    get_project_member
)

from src.repositories.task_list_repository import (
    get_task_list_by_id,
    get_task_list_by_name,
    get_task_list_member
)

from src.repositories.user_repository import (
    get_user_by_id
)


# =========================================================
# CREATE TASK LIST
# =========================================================

def create_task_list(
    db: Session,
    current_user,
    project_id: int,
    name: str,
    description: str | None
):

    project = get_project_by_id(
        db,
        project_id
    )

    if project is None:

        return None, "Project not found."


    if not project.is_active:

        return None, "Project is inactive."


    existing = get_task_list_by_name(
        db,
        project_id,
        name
    )

    if existing:

        return None, (
            "Task list with this name "
            "already exists in this project."
        )


    task_list = TaskList(
        project_id=project_id,
        name=name.strip(),
        description=description,
        owner_id=current_user.id,
        is_active=True
    )

    db.add(task_list)

    db.flush()


    owner_member = TaskListMember(
        task_list_id=task_list.id,
        user_id=current_user.id,
        member_role=ProjectMemberRole.owner
    )

    db.add(owner_member)

    db.commit()

    db.refresh(task_list)

    return task_list, None


# =========================================================
# CHECK ACCESS
# =========================================================

def can_access_task_list(
    db: Session,
    current_user,
    task_list_id: int
):

    if current_user.role == UserRole.admin:

        return True


    member = get_task_list_member(
        db,
        task_list_id,
        current_user.id
    )

    return member is not None


# =========================================================
# UPDATE TASK LIST
# =========================================================

def update_task_list(
    db: Session,
    task_list_id: int,
    task_list_data
):

    task_list = get_task_list_by_id(
        db,
        task_list_id
    )

    if task_list is None:

        return None, "Task list not found."


    updates = task_list_data.model_dump(
        exclude_unset=True
    )


    if "name" in updates:

        existing = get_task_list_by_name(
            db,
            task_list.project_id,
            updates["name"]
        )

        if (
            existing
            and existing.id != task_list.id
        ):

            return None, (
                "Another task list with "
                "this name already exists."
            )


    for key, value in updates.items():

        setattr(
            task_list,
            key,
            value
        )


    db.commit()

    db.refresh(task_list)

    return task_list, None


# =========================================================
# ADD MEMBER
# =========================================================

def add_task_list_member(
    db: Session,
    task_list_id: int,
    user_id: int,
    member_role: ProjectMemberRole
):

    task_list = get_task_list_by_id(
        db,
        task_list_id
    )

    if task_list is None:

        return None, "Task list not found."


    user = get_user_by_id(
        db,
        user_id
    )

    if user is None:

        return None, "User not found."


    if member_role == ProjectMemberRole.owner:

        return None, (
            "Owner role cannot be assigned "
            "through this endpoint."
        )


    project_member = get_project_member(
        db,
        task_list.project_id,
        user_id
    )

    if project_member is None:

        return None, (
            "User must first be a "
            "member of the project."
        )


    existing = get_task_list_member(
        db,
        task_list_id,
        user_id
    )

    if existing:

        return None, (
            "User is already a "
            "task list member."
        )


    member = TaskListMember(
        task_list_id=task_list_id,
        user_id=user_id,
        member_role=member_role
    )

    db.add(member)

    db.commit()

    db.refresh(member)

    return member, None


# =========================================================
# REMOVE MEMBER
# =========================================================

def remove_task_list_member(
    db: Session,
    task_list_id: int,
    user_id: int
):

    task_list = get_task_list_by_id(
        db,
        task_list_id
    )

    if task_list is None:

        return False, "Task list not found."


    if task_list.owner_id == user_id:

        return False, (
            "Task list owner cannot be removed."
        )


    member = get_task_list_member(
        db,
        task_list_id,
        user_id
    )

    if member is None:

        return False, "Member not found."


    db.delete(member)

    db.commit()

    return True, None