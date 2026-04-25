# This file is the entry point for database seeding.
# Run this script when you want to insert the sample development data.

from app.db.seed_data import seed_all
from app.db.session import SessionLocal


def main() -> None:
    """
    Create a database session and run the seed process.
    """
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()