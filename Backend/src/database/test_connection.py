from sqlalchemy import text

from src.database.connection import engine


def test_connection():

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text(
                    """
                    SELECT
                        current_database(),
                        current_user
                    """
                )
            )

            row = result.fetchone()

            print("Database connection successful.")
            print(f"Database : {row[0]}")
            print(f"User     : {row[1]}")

    except Exception as error:

        print("Database connection failed.")
        print(error)


if __name__ == "__main__":
    test_connection()