from sqlalchemy import (
    func,
    select
)

from sqlalchemy.orm import Session

from src.db_models.project import (
    Project,
    ProjectMember,
    ProjectInvitation
)


def get_project_by_id(
    db: Session,
    project_id: int
):

    return db.scalar(
        select(Project)
        .where(
            Project.id == project_id
        )
    )


def get_project_by_name(
    db: Session,
    name: str
):

    return db.scalar(
        select(Project)
        .where(
            func.lower(Project.name)
            == name.strip().lower()
        )
    )


def get_all_projects(
    db: Session
):

    return db.scalars(
        select(Project)
        .order_by(Project.id)
    ).all()


def get_projects_for_user(
    db: Session,
    user_id: int
):

    statement = (
        select(Project)
        .join(
            ProjectMember,
            ProjectMember.project_id
            == Project.id
        )
        .where(
            ProjectMember.user_id == user_id,
            Project.is_active.is_(True)
        )
        .order_by(Project.id)
    )

    return db.scalars(
        statement
    ).all()


def get_project_member(
    db: Session,
    project_id: int,
    user_id: int
):

    return db.scalar(
        select(ProjectMember)
        .where(
            ProjectMember.project_id
            == project_id,

            ProjectMember.user_id
            == user_id
        )
    )


def get_project_members(
    db: Session,
    project_id: int
):

    return db.scalars(
        select(ProjectMember)
        .where(
            ProjectMember.project_id
            == project_id
        )
        .order_by(ProjectMember.id)
    ).all()


def get_invitation_by_id(
    db: Session,
    invitation_id: int
):

    return db.scalar(
        select(ProjectInvitation)
        .where(
            ProjectInvitation.id
            == invitation_id
        )
    )


def get_project_user_invitation(
    db: Session,
    project_id: int,
    user_id: int
):

    return db.scalar(
        select(ProjectInvitation)
        .where(
            ProjectInvitation.project_id
            == project_id,

            ProjectInvitation.invited_user_id
            == user_id
        )
    )


def get_user_invitations(
    db: Session,
    user_id: int
):

    return db.scalars(
        select(ProjectInvitation)
        .where(
            ProjectInvitation.invited_user_id
            == user_id
        )
        .order_by(
            ProjectInvitation.created_at.desc()
        )
    ).all()