from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from src.config.settings import settings
from src.database.connection import get_db

from src.db_models.auth import User

from src.dependencies.auth_dependencies import (
    get_current_user
)

from src.schemas.user_schema import (
    UserCreate,
    UserResponse
)

from src.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterResponse,
    RefreshTokenRequest,
    AccessTokenResponse,
    VerifyEmailRequest,
    ResendVerificationRequest,
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    LogoutRequest,
    DeactivateAccountRequest,
    ReactivateAccountRequest,
    MessageResponse
)

from src.services.user_service import (
    create_user
)

from src.services.auth_service import (
    authenticate_user,
    create_login_tokens,
    refresh_access_token,
    generate_email_verification_token,
    verify_email,
    create_password_reset_token,
    reset_password,
    logout_user,
    deactivate_account,
    reactivate_account
)

from src.repositories.user_repository import (
    get_user_by_email
)

from src.utils.validators import (
    password_errors
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =========================================================
# REGISTER
# =========================================================

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    errors = password_errors(
        user_data.password
    )

    if errors:

        raise HTTPException(
            status_code=400,
            detail=errors
        )


    user, error = create_user(
        db=db,
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )


    if error:

        raise HTTPException(
            status_code=409,
            detail=error
        )


    verification_token = (
        generate_email_verification_token(
            db,
            user.id
        )
    )


    return {
        "message": (
            "Registration successful. "
            "Please verify your email."
        ),
        "user": user,
        "verification_token": (
            verification_token
            if settings.debug
            else None
        )
    }


# =========================================================
# VERIFY EMAIL
# =========================================================

@router.post(
    "/verify-email",
    response_model=MessageResponse
)
def verify_email_route(
    request: VerifyEmailRequest,
    db: Session = Depends(get_db)
):

    success = verify_email(
        db,
        request.token
    )

    if not success:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid or expired "
                "verification token."
            )
        )


    return {
        "message": "Email verified successfully."
    }


# =========================================================
# RESEND VERIFICATION
# =========================================================

@router.post(
    "/resend-verification"
)
def resend_verification(
    request: ResendVerificationRequest,
    db: Session = Depends(get_db)
):

    user = get_user_by_email(
        db,
        request.email
    )


    if user is None:

        return {
            "message": (
                "If the account exists, "
                "a verification link has been generated."
            )
        }


    if user.is_email_verified:

        return {
            "message": (
                "Email is already verified."
            )
        }


    token = generate_email_verification_token(
        db,
        user.id
    )


    response = {
        "message": (
            "Verification token generated."
        )
    }


    if settings.debug:

        response["verification_token"] = token


    return response


# =========================================================
# LOGIN
# =========================================================

@router.post(
    "/login",
    response_model=LoginResponse
)
def login_user(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    user, error = authenticate_user(
        db=db,
        email=login_data.email,
        password=login_data.password
    )


    if error == "invalid":

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    if error == "inactive":

        raise HTTPException(
            status_code=403,
            detail="Account is deactivated."
        )


    if error == "unverified":

        raise HTTPException(
            status_code=403,
            detail="Please verify your email."
        )


    access_token, refresh_token = (
        create_login_tokens(
            db,
            user
        )
    )


    return {
        "message": "Login successful.",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }


# =========================================================
# REFRESH
# =========================================================

@router.post(
    "/refresh",
    response_model=AccessTokenResponse
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):

    token = refresh_access_token(
        db,
        request.refresh_token
    )


    if token is None:

        raise HTTPException(
            status_code=401,
            detail=(
                "Invalid or expired "
                "refresh token."
            )
        )


    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =========================================================
# CURRENT USER
# =========================================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    )
):

    return current_user


# =========================================================
# FORGOT PASSWORD
# =========================================================

@router.post(
    "/forgot-password",
    response_model=ForgotPasswordResponse
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    token = create_password_reset_token(
        db,
        request.email
    )


    return {
        "message": (
            "If the account exists, "
            "password reset instructions "
            "have been generated."
        ),
        "reset_token": (
            token
            if settings.debug
            else None
        )
    }


# =========================================================
# RESET PASSWORD
# =========================================================

@router.post(
    "/reset-password",
    response_model=MessageResponse
)
def reset_password_route(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    errors = password_errors(
        request.new_password
    )

    if errors:

        raise HTTPException(
            status_code=400,
            detail=errors
        )


    success = reset_password(
        db,
        request.token,
        request.new_password
    )


    if not success:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid or expired "
                "password reset token."
            )
        )


    return {
        "message": "Password reset successfully."
    }


# =========================================================
# LOGOUT
# =========================================================

@router.post(
    "/logout",
    response_model=MessageResponse
)
def logout(
    request: LogoutRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    logout_user(
        db,
        request.refresh_token
    )


    return {
        "message": "Logout successful."
    }


# =========================================================
# DEACTIVATE ACCOUNT
# =========================================================

@router.post(
    "/deactivate",
    response_model=MessageResponse
)
def deactivate(
    request: DeactivateAccountRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    success = deactivate_account(
        db,
        current_user,
        request.password
    )


    if not success:

        raise HTTPException(
            status_code=400,
            detail="Incorrect password."
        )


    return {
        "message": (
            "Account deactivated successfully."
        )
    }


# =========================================================
# REACTIVATE ACCOUNT
# =========================================================

@router.post(
    "/reactivate",
    response_model=MessageResponse
)
def reactivate(
    request: ReactivateAccountRequest,
    db: Session = Depends(get_db)
):

    user, error = reactivate_account(
        db,
        request.email,
        request.password
    )


    if error == "invalid":

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )


    if error == "already_active":

        return {
            "message": "Account is already active."
        }


    return {
        "message": (
            "Account reactivated successfully. "
            "You can now login."
        )
    }