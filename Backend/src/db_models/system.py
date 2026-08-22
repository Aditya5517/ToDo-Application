from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func
)

from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base


class Notification(Base):

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id")
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id")
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    message: Mapped[str | None] = mapped_column(
        Text
    )

    notification_type: Mapped[str | None] = mapped_column(
        String(50)
    )

    is_read: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    read_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )


class ActivityLog(Base):

    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id")
    )

    task_id: Mapped[int | None] = mapped_column(
        ForeignKey("tasks.id")
    )

    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id")
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_type: Mapped[str | None] = mapped_column(
        String(50)
    )

    entity_id: Mapped[int | None] = mapped_column(
        Integer
    )

    old_value: Mapped[str | None] = mapped_column(
        Text
    )

    new_value: Mapped[str | None] = mapped_column(
        Text
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )