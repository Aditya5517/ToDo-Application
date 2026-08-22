from sqlalchemy import select

from src.database.connection import SessionLocal
from src.db_models.auth import User


def test_users():

    db = SessionLocal()

    try:

        statement = (
            select(User)
            .order_by(User.id)
        )

        users = db.scalars(
            statement
        ).all()

        print("\nUsers from PostgreSQL:\n")

        for user in users:

            print(
                f"{user.id} | "
                f"{user.name} | "
                f"{user.email} | "
                f"{user.role.value}"
            )

    finally:

        db.close()


if __name__ == "__main__":
    test_users()