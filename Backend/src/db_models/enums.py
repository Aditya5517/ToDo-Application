from enum import Enum


class UserRole(str, Enum):
    admin = "admin"
    user = "user"


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    blocked = "blocked"
    completed = "completed"
    cancelled = "cancelled"


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class ProjectMemberRole(str, Enum):
    owner = "owner"
    editor = "editor"
    viewer = "viewer"
    member = "member"


class InvitationStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    expired = "expired"


class AssignmentStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class ChatAccessStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class ChatMemberAccessType(str, Enum):
    project_member = "project_member"
    approved_request = "approved_request"