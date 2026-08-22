from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from src.db_models.enums import (
    InvitationStatus,
    ProjectMemberRole
)


class ProjectCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=150
    )

    description: str | None = None


class ProjectUpdate(BaseModel):

    name: str | None = None

    description: str | None = None

    is_active: bool | None = None


class ProjectResponse(BaseModel):

    id: int

    name: str

    description: str | None

    owner_id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ProjectMemberCreate(BaseModel):

    user_id: int

    member_role: ProjectMemberRole = (
        ProjectMemberRole.member
    )


class ProjectMemberResponse(BaseModel):

    id: int

    project_id: int

    user_id: int

    member_role: ProjectMemberRole

    joined_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ProjectInvitationCreate(BaseModel):

    invited_user_id: int

    member_role: ProjectMemberRole = (
        ProjectMemberRole.member
    )


class ProjectInvitationResponse(BaseModel):

    id: int

    project_id: int

    invited_user_id: int

    invited_by: int

    member_role: ProjectMemberRole

    status: InvitationStatus

    expires_at: datetime

    created_at: datetime

    responded_at: datetime | None

    model_config = ConfigDict(
        from_attributes=True
    )