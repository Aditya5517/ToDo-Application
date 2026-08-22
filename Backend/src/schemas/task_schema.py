from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)

from src.db_models.enums import (
    TaskPriority,
    TaskStatus
)


class TaskCreate(BaseModel):

    task_list_id: int

    parent_task_id: int | None = None

    title: str = Field(
        min_length=1,
        max_length=200
    )

    description: str | None = None

    status: TaskStatus = TaskStatus.pending

    priority: TaskPriority = TaskPriority.medium

    start_date: datetime | None = None

    due_date: datetime

    is_recurring: bool = False


class TaskUpdate(BaseModel):

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200
    )

    description: str | None = None

    status: TaskStatus | None = None

    priority: TaskPriority | None = None

    start_date: datetime | None = None

    due_date: datetime | None = None

    is_recurring: bool | None = None


class TaskResponse(BaseModel):

    id: int

    task_list_id: int

    parent_task_id: int | None

    title: str

    description: str | None

    status: TaskStatus

    priority: TaskPriority

    created_by: int

    start_date: datetime | None

    due_date: datetime

    is_recurring: bool

    completed_by: int | None

    completed_at: datetime | None

    is_archived: bool

    archived_by: int | None

    archived_at: datetime | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )