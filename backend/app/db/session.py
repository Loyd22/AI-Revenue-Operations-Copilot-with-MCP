# This file creates the SQLAlchemy database engine and session factory.
# The engine is the main connection to PostgreSQL.
# The session is what the app will use later to talk to the database.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create the SQLAlchemy engine using the DATABASE_URL from the .env file.
engine = create_engine(settings.database_url, future=True)

# Create a reusable session factory for database operations.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db():
    """
    Dependency for getting a database session inside FastAPI routes.

    Later, API endpoints will use this to access the database safely.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()