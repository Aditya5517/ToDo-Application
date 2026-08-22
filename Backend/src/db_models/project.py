from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func
)

from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base
from src.db_models.enums import (
    InvitationStatus,
    ProjectMemberRole
)


project_member_role_enum = PGEnum(
    ProjectMemberRole,
    name="project_member_role",
    create_type=False
)

invitation_status_enum = PGEnum(
    InvitationStatus,
    name="invitation_status",
    create_type=False
)


class Project(Base):

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class ProjectMember(Base):

    __tablename__ = "project_members"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "user_id",
            name="uq_project_member"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    member_role: Mapped[ProjectMemberRole] = mapped_column(
        project_member_role_enum,
        nullable=False,
        default=ProjectMemberRole.member
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class TaskList(Base):

    __tablename__ = "task_lists"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class TaskListMember(Base):

    __tablename__ = "task_list_members"

    __table_args__ = (
        UniqueConstraint(
            "task_list_id",
            "user_id",
            name="uq_task_list_member"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_list_id: Mapped[int] = mapped_column(
        ForeignKey("task_lists.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    member_role: Mapped[ProjectMemberRole] = mapped_column(
        project_member_role_enum,
        nullable=False,
        default=ProjectMemberRole.viewer
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class ProjectInvitation(Base):

    __tablename__ = "project_invitations"

    __table_args__ = (
        UniqueConstraint(
            "project_id",
            "invited_user_id",
            name="uq_project_invitation"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False
    )

    invited_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    invited_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    member_role: Mapped[ProjectMemberRole] = mapped_column(
        project_member_role_enum,
        nullable=False,
        default=ProjectMemberRole.member
    )

    status: Mapped[InvitationStatus] = mapped_column(
        invitation_status_enum,
        nullable=False,
        default=InvitationStatus.pending
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    responded_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )