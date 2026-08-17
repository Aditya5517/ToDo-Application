from pydantic import BaseModel,EmailStr
from typing import Literal
from datetime import datetime



class TaskCreate(BaseModel):
    title: str
    priority: str
    status: str


class TaskUpdate(BaseModel):
    title: str | None = None
    priority: str | None = None
    status: str | None = None


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: str
    role: Literal["user", "admin"]
    created_at: datetime
    tasks_assigned: int
    tasks_completed: int
    is_active: bool

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    username: str
    role: str

class LogoutResponse(BaseModel):
    message: str