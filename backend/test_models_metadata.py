# This script checks whether SQLAlchemy sees all model tables.

from app.db.base import Base


def main():
    table_names = sorted(Base.metadata.tables.keys())
    print("Registered tables:")
    for name in table_names:
        print("-", name)


if __name__ == "__main__":
    main()