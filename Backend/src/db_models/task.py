from datetime import date, datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
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
    AssignmentStatus,
    TaskPriority,
    TaskStatus
)


task_status_enum = PGEnum(
    TaskStatus,
    name="task_status",
    create_type=False
)

task_priority_enum = PGEnum(
    TaskPriority,
    name="task_priority",
    create_type=False
)

assignment_status_enum = PGEnum(
    AssignmentStatus,
    name="assignment_status",
    create_type=False
)


class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_list_id: Mapped[int] = mapped_column(
        ForeignKey("task_lists.id"),
        nullable=False
    )

    parent_task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id")
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    status: Mapped[TaskStatus] = mapped_column(
        task_status_enum,
        nullable=False,
        default=TaskStatus.pending
    )

    priority: Mapped[TaskPriority] = mapped_column(
        task_priority_enum,
        nullable=False,
        default=TaskPriority.medium
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    start_date: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    due_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    is_recurring: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    completed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id")
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    archived_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id")
    )

    archived_at: Mapped[datetime | None] = mapped_column(
        DateTime
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


class TaskAssignment(Base):

    __tablename__ = "task_assignments"

    __table_args__ = (
        UniqueConstraint(
            "task_id",
            "user_id",
            name="uq_task_assignment"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    assigned_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    assignment_status: Mapped[AssignmentStatus] = mapped_column(
        assignment_status_enum,
        nullable=False,
        default=AssignmentStatus.pending
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    responded_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    response_note: Mapped[str | None] = mapped_column(
        Text
    )

    notes: Mapped[str | None] = mapped_column(
        Text
    )


class TaskComment(Base):

    __tablename__ = "task_comments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    comment: Mapped[str] = mapped_column(
        Text,
        nullable=False
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


class TaskAttachment(Base):

    __tablename__ = "task_attachments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    file_type: Mapped[str | None] = mapped_column(
        String(100)
    )

    file_size: Mapped[int | None] = mapped_column(
        BigInteger
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class TaskDependency(Base):

    __tablename__ = "task_dependencies"

    __table_args__ = (
        UniqueConstraint(
            "task_id",
            "depends_on_task_id",
            name="uq_task_dependency"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    depends_on_task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    dependency_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="blocks"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class TaskChecklistItem(Base):

    __tablename__ = "task_checklist_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    completed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id")
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime
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


class Reminder(Base):

    __tablename__ = "reminders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    remind_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    reminder_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="notification"
    )

    is_sent: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )


class RecurringTaskRule(Base):

    __tablename__ = "recurring_task_rules"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    task_id: Mapped[int] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=False,
        unique=True
    )

    frequency: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    interval_value: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    day_of_week: Mapped[int | None] = mapped_column(
        Integer
    )

    day_of_month: Mapped[int | None] = mapped_column(
        Integer
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date | None] = mapped_column(
        Date
    )

    next_run_at: Mapped[datetime | None] = mapped_column(
        DateTime
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