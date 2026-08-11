from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    priority: str
    status: str


class TaskUpdate(BaseModel):
    title: str | None = None
    priority: str | None = None
    status: str | None = None