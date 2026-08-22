from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func
)

from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import Base
from src.db_models.enums import (
    ChatAccessStatus,
    ChatMemberAccessType
)


chat_access_status_enum = PGEnum(
    ChatAccessStatus,
    name="chat_access_status",
    create_type=False
)

chat_member_access_type_enum = PGEnum(
    ChatMemberAccessType,
    name="chat_member_access_type",
    create_type=False
)


class ProjectChatRoom(Base):

    __tablename__ = "project_chat_rooms"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"),
        nullable=False,
        unique=True
    )

    created_by: Mapped[int] = mapped_column(
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


class ProjectChatAccessRequest(Base):

    __tablename__ = "project_chat_access_requests"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    chat_room_id: Mapped[int] = mapped_column(
        ForeignKey("project_chat_rooms.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    status: Mapped[ChatAccessStatus] = mapped_column(
        chat_access_status_enum,
        nullable=False,
        default=ChatAccessStatus.pending
    )

    requested_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    reviewed_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id")
    )

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )


class ProjectChatMember(Base):

    __tablename__ = "project_chat_members"

    __table_args__ = (
        UniqueConstraint(
            "chat_room_id",
            "user_id",
            name="uq_chat_room_member"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    chat_room_id: Mapped[int] = mapped_column(
        ForeignKey("project_chat_rooms.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    access_type: Mapped[ChatMemberAccessType] = mapped_column(
        chat_member_access_type_enum,
        nullable=False
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )


class ChatMessage(Base):

    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    chat_room_id: Mapped[int] = mapped_column(
        ForeignKey("project_chat_rooms.id"),
        nullable=False
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    message_text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    reply_to_message_id: Mapped[int | None] = mapped_column(
        ForeignKey("chat_messages.id")
    )

    sent_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    is_edited: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    edited_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )


class MessageReceipt(Base):

    __tablename__ = "message_receipts"

    __table_args__ = (
        UniqueConstraint(
            "message_id",
            "user_id",
            name="uq_message_receipt"
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True
    )

    message_id: Mapped[int] = mapped_column(
        ForeignKey("chat_messages.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )

    seen_at: Mapped[datetime | None] = mapped_column(
        DateTime
    )