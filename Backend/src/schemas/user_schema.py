from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)

from src.db_models.enums import UserRole


class UserCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=8
    )


class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: UserRole

    is_active: bool

    is_email_verified: bool

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )