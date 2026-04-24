# This file creates the main SQLAlchemy base class
# and imports all models so metadata is registered.

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so SQLAlchemy metadata knows about all tables.
import app.models  # noqa: F401, E402