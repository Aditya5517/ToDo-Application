from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from src.database.connection import get_db

from src.db_models.auth import User

from src.dependencies.auth_dependencies import (
    get_current_user,
    require_admin
)

from src.repositories.project_repository import (
    get_project_by_id,
    get_project_members,
    get_user_invitations
)

from src.schemas.project_schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectMemberCreate,
    ProjectMemberResponse,
    ProjectInvitationCreate,
    ProjectInvitationResponse
)

from src.services.project_service import (
    create_project,
    list_projects,
    can_access_project,
    update_project,
    deactivate_project,
    add_project_member,
    remove_project_member,
    create_project_invitation,
    accept_project_invitation,
    reject_project_invitation
)


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# =========================================================
# CREATE PROJECT
# ADMIN ONLY
# =========================================================

@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    project, error = create_project(
        db=db,
        current_user=admin,
        name=project_data.name,
        description=project_data.description
    )


    if error:

        raise HTTPException(
            status_code=409,
            detail=error
        )


    return project


# =========================================================
# LIST PROJECTS
# =========================================================

@router.get(
    "",
    response_model=list[ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return list_projects(
        db,
        current_user
    )


# =========================================================
# MY INVITATIONS
# =========================================================

@router.get(
    "/invitations/me",
    response_model=list[
        ProjectInvitationResponse
    ]
)
def my_project_invitations(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return get_user_invitations(
        db,
        current_user.id
    )


# =========================================================
# ACCEPT INVITATION
# =========================================================

@router.post(
    "/invitations/{invitation_id}/accept",
    response_model=ProjectInvitationResponse
)
def accept_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    invitation, error = (
        accept_project_invitation(
            db,
            invitation_id,
            current_user
        )
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return invitation


# =========================================================
# REJECT INVITATION
# =========================================================

@router.post(
    "/invitations/{invitation_id}/reject",
    response_model=ProjectInvitationResponse
)
def reject_invitation(
    invitation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    invitation, error = (
        reject_project_invitation(
            db,
            invitation_id,
            current_user
        )
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return invitation


# =========================================================
# GET PROJECT
# =========================================================

@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    project = get_project_by_id(
        db,
        project_id
    )


    if project is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )


    if not can_access_project(
        db,
        current_user,
        project_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Project access denied."
        )


    return project


# =========================================================
# UPDATE PROJECT
# ADMIN ONLY
# =========================================================

@router.patch(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_existing_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    project = update_project(
        db,
        project_id,
        project_data
    )


    if project is None:

        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )


    return project


# =========================================================
# DEACTIVATE PROJECT
# ADMIN ONLY
# =========================================================

@router.delete(
    "/{project_id}"
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    success = deactivate_project(
        db,
        project_id
    )


    if not success:

        raise HTTPException(
            status_code=404,
            detail="Project not found."
        )


    return {
        "message": (
            "Project deactivated successfully."
        )
    }


# =========================================================
# PROJECT MEMBERS
# =========================================================

@router.get(
    "/{project_id}/members",
    response_model=list[
        ProjectMemberResponse
    ]
)
def project_members(
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


    return get_project_members(
        db,
        project_id
    )


# =========================================================
# ADD MEMBER
# ADMIN ONLY
# =========================================================

@router.post(
    "/{project_id}/members",
    response_model=ProjectMemberResponse
)
def add_member(
    project_id: int,
    member_data: ProjectMemberCreate,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    member, error = add_project_member(
        db=db,
        project_id=project_id,
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
    "/{project_id}/members/{user_id}"
)
def remove_member(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)
):

    success, error = (
        remove_project_member(
            db,
            project_id,
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
            "Project member removed successfully."
        )
    }


# =========================================================
# INVITE USER
# ADMIN ONLY
# =========================================================

@router.post(
    "/{project_id}/invitations",
    response_model=ProjectInvitationResponse
)
def invite_user(
    project_id: int,
    invitation_data: ProjectInvitationCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):

    invitation, error = (
        create_project_invitation(
            db=db,
            project_id=project_id,
            invited_user_id=(
                invitation_data.invited_user_id
            ),
            invited_by=admin.id,
            member_role=(
                invitation_data.member_role
            )
        )
    )


    if error:

        raise HTTPException(
            status_code=400,
            detail=error
        )


    return invitation