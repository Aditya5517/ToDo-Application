from datetime import datetime, timezone
from src.services.file_handler import (
    load_users,
    save_users
)
from src.utils.security import hash_password
from src.utils.logs import logger

def create_user(
    username: str,
    email: str,
    password: str,
    phone: str
):

    users = load_users()

    # =========================
    # CHECK USERNAME
    # =========================

    for user in users:

        if user["username"].lower() == username.lower():

            return None, "Username already exists."

    # =========================
    # CHECK EMAIL
    # =========================

    for user in users:

        if user["email"].lower() == email.lower():

            return None, "Email already exists."

    # =========================
    # GENERATE USER ID
    # =========================

    if users:

        user_id = max(
            user["id"]
            for user in users
        ) + 1

    else:

        user_id = 1

    # =========================
    # CREATE USER
    # =========================

    new_user = {

        "id": user_id,

        "username": username.strip(),

        "email": email.strip().lower(),

        "password": hash_password(password),

        "phone": phone.strip(),

        "role": "user",

        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),

        "tasks_assigned": 0,

        "tasks_completed": 0,

        "is_active": True
    }
    users.append(new_user)
    save_users(users)
    logger.info(
        f"User created | ID={user_id} | "
        f"username={username}"
    )
    return new_user, None