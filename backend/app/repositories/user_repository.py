# This file contains the database logic for reading and writing users.
# We keep database queries separate from route logic and service logic.

from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User


class UserRepository:
    """
    Repository for user-related database operations.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        """
        Find one user by email.
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, user_id: int) -> User | None:
        """
        Find one user by ID.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def get_role_by_name(self, role_name: str) -> Role | None:
        """
        Find one role by its name.
        """
        return self.db.query(Role).filter(Role.name == role_name).first()

    def create_user(
        self,
        full_name: str,
        email: str,
        password_hash: str,
        role_id: int,
    ) -> User:
        """
        Create and save a new user.
        """
        user = User(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role_id=role_id,
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user