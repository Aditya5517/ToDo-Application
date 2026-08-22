from datetime import (
    datetime,
    timedelta,
    timezone
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db_models.project import (
    Project,
    ProjectMember,
    ProjectInvitation
)

from src.db_models.chat import (
    ProjectChatRoom,
    ProjectChatMember
)

from src.db_models.enums import (
    ChatMemberAccessType,
    InvitationStatus,
    ProjectMemberRole,
    UserRole
)

from src.repositories.project_repository import (
    get_all_projects,
    get_project_by_id,
    get_project_by_name,
    get_project_member,
    get_project_members,
    get_projects_for_user,
    get_invitation_by_id,
    get_project_user_invitation,
    get_user_invitations
)

from src.repositories.user_repository import (
    get_user_by_id
)


def utc_now():

    return datetime.now(
        timezone.utc
    ).replace(
        tzinfo=None
    )


# =========================================================
# CREATE PROJECT
# =========================================================

def create_project(
    db: Session,
    current_user,
    name: str,
    description: str | None
):

    existing = get_project_by_name(
        db,
        name
    )

    if existing:

        return None, "Project name already exists."


    project = Project(
        name=name.strip(),
        description=description,
        owner_id=current_user.id,
        is_active=True
    )

    db.add(project)
    db.flush()


    owner_member = ProjectMember(
        project_id=project.id,
        user_id=current_user.id,
        member_role=ProjectMemberRole.owner
    )

    db.add(owner_member)


    chat_room = ProjectChatRoom(
        project_id=project.id,
        created_by=current_user.id
    )

    db.add(chat_room)
    db.flush()


    chat_member = ProjectChatMember(
        chat_room_id=chat_room.id,
        user_id=current_user.id,
        access_type=(
            ChatMemberAccessType.project_member
        )
    )

    db.add(chat_member)


    db.commit()
    db.refresh(project)

    return project, None


# =========================================================
# LIST PROJECTS
# =========================================================

def list_projects(
    db: Session,
    current_user
):

    if current_user.role == UserRole.admin:

        return get_all_projects(db)


    return get_projects_for_user(
        db,
        current_user.id
    )


# =========================================================
# CHECK PROJECT ACCESS
# =========================================================

def can_access_project(
    db: Session,
    current_user,
    project_id: int
):

    if current_user.role == UserRole.admin:

        return True


    member = get_project_member(
        db,
        project_id,
        current_user.id
    )

    return member is not None


# =========================================================
# UPDATE PROJECT
# =========================================================

def update_project(
    db: Session,
    project_id: int,
    project_data
):

    project = get_project_by_id(
        db,
        project_id
    )

    if project is None:

        return None


    updates = project_data.model_dump(
        exclude_unset=True
    )


    for key, value in updates.items():

        setattr(
            project,
            key,
            value
        )


    db.commit()
    db.refresh(project)

    return project


# =========================================================
# DEACTIVATE PROJECT
# =========================================================

def deactivate_project(
    db: Session,
    project_id: int
):

    project = get_project_by_id(
        db,
        project_id
    )

    if project is None:

        return False


    project.is_active = False


    room = db.scalar(
        select(ProjectChatRoom)
        .where(
            ProjectChatRoom.project_id
            == project_id
        )
    )

    if room:

        room.is_active = False


    db.commit()

    return True


# =========================================================
# ADD MEMBER
# =========================================================

def add_project_member(
    db: Session,
    project_id: int,
    user_id: int,
    member_role: ProjectMemberRole
):

    project = get_project_by_id(
        db,
        project_id
    )

    if project is None:

        return None, "Project not found."


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


    existing = get_project_member(
        db,
        project_id,
        user_id
    )

    if existing:

        return None, (
            "User is already a project member."
        )


    member = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        member_role=member_role
    )

    db.add(member)


    room = db.scalar(
        select(ProjectChatRoom)
        .where(
            ProjectChatRoom.project_id
            == project_id
        )
    )


    if room:

        chat_member = db.scalar(
            select(ProjectChatMember)
            .where(
                ProjectChatMember.chat_room_id
                == room.id,

                ProjectChatMember.user_id
                == user_id
            )
        )


        if chat_member:

            chat_member.is_active = True

            chat_member.access_type = (
                ChatMemberAccessType.project_member
            )

            chat_member.expires_at = None

        else:

            db.add(
                ProjectChatMember(
                    chat_room_id=room.id,
                    user_id=user_id,
                    access_type=(
                        ChatMemberAccessType.project_member
                    )
                )
            )


    db.commit()
    db.refresh(member)

    return member, None


# =========================================================
# REMOVE MEMBER
# =========================================================

def remove_project_member(
    db: Session,
    project_id: int,
    user_id: int
):

    project = get_project_by_id(
        db,
        project_id
    )

    if project is None:

        return False, "Project not found."


    if project.owner_id == user_id:

        return False, (
            "Project owner cannot be removed."
        )


    member = get_project_member(
        db,
        project_id,
        user_id
    )

    if member is None:

        return False, "Member not found."


    db.delete(member)


    room = db.scalar(
        select(ProjectChatRoom)
        .where(
            ProjectChatRoom.project_id
            == project_id
        )
    )


    if room:

        chat_member = db.scalar(
            select(ProjectChatMember)
            .where(
                ProjectChatMember.chat_room_id
                == room.id,

                ProjectChatMember.user_id
                == user_id
            )
        )

        if chat_member:

            chat_member.is_active = False


    db.commit()

    return True, None


# =========================================================
# CREATE PROJECT INVITATION
# =========================================================

def create_project_invitation(
    db: Session,
    project_id: int,
    invited_user_id: int,
    invited_by: int,
    member_role: ProjectMemberRole
):

    project = get_project_by_id(
        db,
        project_id
    )

    if project is None:

        return None, "Project not found."


    user = get_user_by_id(
        db,
        invited_user_id
    )

    if user is None:

        return None, "User not found."


    if get_project_member(
        db,
        project_id,
        invited_user_id
    ):

        return None, (
            "User is already a project member."
        )


    if member_role == ProjectMemberRole.owner:

        return None, (
            "Owner role cannot be invited."
        )


    expires_at = utc_now() + timedelta(
        days=7
    )


    invitation = get_project_user_invitation(
        db,
        project_id,
        invited_user_id
    )


    if invitation:

        invitation.invited_by = invited_by
        invitation.member_role = member_role
        invitation.status = (
            InvitationStatus.pending
        )
        invitation.expires_at = expires_at
        invitation.responded_at = None

    else:

        invitation = ProjectInvitation(
            project_id=project_id,
            invited_user_id=invited_user_id,
            invited_by=invited_by,
            member_role=member_role,
            status=InvitationStatus.pending,
            expires_at=expires_at
        )

        db.add(invitation)


    db.commit()
    db.refresh(invitation)

    return invitation, None


# =========================================================
# ACCEPT INVITATION
# =========================================================

def accept_project_invitation(
    db: Session,
    invitation_id: int,
    current_user
):

    invitation = get_invitation_by_id(
        db,
        invitation_id
    )


    if invitation is None:

        return None, "Invitation not found."


    if (
        invitation.invited_user_id
        != current_user.id
    ):

        return None, (
            "This invitation does not "
            "belong to you."
        )


    if invitation.status != InvitationStatus.pending:

        return None, (
            "Invitation is not pending."
        )


    if invitation.expires_at <= utc_now():

        invitation.status = (
            InvitationStatus.expired
        )

        db.commit()

        return None, "Invitation has expired."


    member, error = add_project_member(
        db=db,
        project_id=invitation.project_id,
        user_id=current_user.id,
        member_role=invitation.member_role
    )


    if error:

        return None, error


    invitation.status = (
        InvitationStatus.accepted
    )

    invitation.responded_at = utc_now()

    db.commit()

    return invitation, None


# =========================================================
# REJECT INVITATION
# =========================================================

def reject_project_invitation(
    db: Session,
    invitation_id: int,
    current_user
):

    invitation = get_invitation_by_id(
        db,
        invitation_id
    )


    if invitation is None:

        return None, "Invitation not found."


    if (
        invitation.invited_user_id
        != current_user.id
    ):

        return None, (
            "This invitation does not "
            "belong to you."
        )


    if invitation.status != InvitationStatus.pending:

        return None, (
            "Invitation is not pending."
        )


    invitation.status = (
        InvitationStatus.rejected
    )

    invitation.responded_at = utc_now()

    db.commit()

    return invitation, None