from getpass import getpass

from sqlalchemy import select

from src.database.connection import (
    SessionLocal
)

from src.db_models.auth import User

from src.db_models.enums import (
    UserRole
)

from src.utils.security import (
    hash_password
)


def set_admin_password():

    email = input(
        "Admin email [admin@example.com]: "
    ).strip().lower()

    if not email:
        email = "admin@example.com"


    password = getpass(
        "Enter new admin password: "
    )


    db = SessionLocal()

    try:

        statement = select(
            User
        ).where(
            User.email == email
        )

        user = db.scalar(
            statement
        )


        if user is None:

            print(
                "Admin user not found."
            )

            return


        user.password_hash = (
            hash_password(password)
        )

        user.role = UserRole.admin

        user.is_active = True


        db.commit()


        print(
            "Admin password updated successfully."
        )


    finally:

        db.close()


if __name__ == "__main__":

    set_admin_password()