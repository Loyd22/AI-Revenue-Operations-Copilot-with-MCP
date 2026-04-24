# This script tests whether the backend can connect to PostgreSQL.
# It runs a very small SQL query: SELECT 1

from sqlalchemy import text

from app.db.session import engine


def test_connection():
    """
    Open a database connection and run a simple query.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful.")
        print("Query result:", result.scalar())


if __name__ == "__main__":
    test_connection()