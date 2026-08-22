from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from src.db_models.enums import (
    ProjectMemberRole
)


class TaskListCreate(BaseModel):

    project_id: int

    name: str = Field(
        min_length=2,
        max_length=150
    )

    description: str | None = None


class TaskListUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: str | None = None

    is_active: bool | None = None


class TaskListResponse(BaseModel):

    id: int

    project_id: int

    name: str

    description: str | None

    owner_id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class TaskListMemberCreate(BaseModel):

    user_id: int

    member_role: ProjectMemberRole = (
        ProjectMemberRole.member
    )


class TaskListMemberResponse(BaseModel):

    id: int

    task_list_id: int

    user_id: int

    member_role: ProjectMemberRole

    joined_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )