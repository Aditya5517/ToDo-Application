from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from src.schemas.user_schema import UserResponse


class LoginRequest(BaseModel):

    email: EmailStr
    password: str


class LoginResponse(BaseModel):

    message: str

    access_token: str
    refresh_token: str

    token_type: str = "bearer"

    user: UserResponse


class RegisterResponse(BaseModel):

    message: str

    user: UserResponse

    # Temporary development-only field.
    verification_token: str | None = None


class RefreshTokenRequest(BaseModel):

    refresh_token: str


class AccessTokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class VerifyEmailRequest(BaseModel):

    token: str


class ResendVerificationRequest(BaseModel):

    email: EmailStr


class ForgotPasswordRequest(BaseModel):

    email: EmailStr


class ForgotPasswordResponse(BaseModel):

    message: str

    # Development/testing only.
    reset_token: str | None = None


class ResetPasswordRequest(BaseModel):

    token: str

    new_password: str = Field(
        min_length=8
    )


class LogoutRequest(BaseModel):

    refresh_token: str


class DeactivateAccountRequest(BaseModel):

    password: str


class ReactivateAccountRequest(BaseModel):

    email: EmailStr

    password: str


class MessageResponse(BaseModel):

    message: str