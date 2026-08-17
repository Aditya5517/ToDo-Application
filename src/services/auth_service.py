from src.services.file_handler import load_users
from src.utils.security import verify_password
from src.utils.logs import logger
from fastapi import HTTPException


def authenticate_user(username: str, password: str):

    users = load_users()

    for user in users:

        if user["username"].lower() == username.strip().lower():

            # Check whether account is active
            if not user["is_active"]:

                logger.warning(
                    f"Login blocked - inactive user | username={username}"
                )

                return None

            # Verify password
            if verify_password(
                password,
                user["password"]
            ):

                logger.info(
                    f"User login successful | username={username}"
                )

                return user

            logger.warning(
                f"Login failed - incorrect password | username={username}"
            )

            return None

    logger.warning(
        f"Login failed - user not found | username={username}"
    )

    return None


def require_admin(user):

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Authentication required."
        )
    if user["role"] != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin access required."
        )
    return user