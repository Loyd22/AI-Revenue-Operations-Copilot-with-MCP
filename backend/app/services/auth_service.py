# This file handles the main login and registration logic of the app.
# In simple words, this is the part that decides:
# - can a new user sign up?
# - is a login valid?
# - what tokens should be given after login?
# - how do we make a new access token later?

from sqlalchemy.orm import Session

# These are helper tools for security-related tasks:
# - create_access_token: makes the short-term login token
# - create_refresh_token: makes the longer-term refresh token
# - hash_password: turns a password into a protected form before saving
# - verify_password: checks if the entered password matches the saved one
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)

# User is the database model for people who can log in.
from app.models.user import User

# UserRepository is the database helper for reading and writing user data.
from app.repositories.user_repository import UserRepository


class AuthService:
    """
    This class is the main auth workflow manager.

    In simple words:
    - it checks if sign up is allowed
    - it checks if login is correct
    - it creates login tokens
    - it handles refresh-token related logic
    """

    def __init__(self, db: Session):
        # Save the database helper so this service can read and write user data.
        self.user_repository = UserRepository(db)

    def register_user(
        self,
        full_name: str,
        email: str,
        password: str,
        role_name: str,
    ) -> User:
        """
        Create a new user account.

        What this does:
        1. Check if the email is already used
        2. Check if the given role exists
        3. Protect the password by hashing it
        4. Save the new user in the database
        """

        # Check if another user already has this email.
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("A user with this email already exists.")

        # Check if the requested role is valid, such as admin or sales_rep.
        role = self.user_repository.get_role_by_name(role_name)
        if role is None:
            raise ValueError("Invalid role.")

        # Convert the plain password into a protected hash before storing it.
        password_hash = hash_password(password)

        # Save the new user in the database and return the created user record.
        return self.user_repository.create_user(
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role_id=role.id,
        )

    def authenticate_user(self, email: str, password: str) -> User:
        """
        Check if a login attempt is valid.

        What this does:
        1. Find the user by email
        2. Make sure the account exists
        3. Make sure the account is active
        4. Check if the password is correct
        5. Return the user if everything is valid
        """

        # Find the user with this email.
        user = self.user_repository.get_by_email(email)
        if user is None:
            raise ValueError("Invalid email or password.")

        # Stop login if the account is disabled/inactive.
        if not user.is_active:
            raise ValueError("This user account is inactive.")

        # Check if the entered password matches the stored password hash.
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password.")

        # Login is valid, so return the user.
        return user

    def create_token_response(self, user: User) -> dict:
        """
        Build the login response after a successful login.

        What this returns:
        - access token: used for normal protected requests
        - refresh token: used to get a new access token later
        - token type
        - basic user information for the frontend
        """

        # Create the short-term token used for most authenticated requests.
        access_token = create_access_token(subject=user.id)

        # Create the longer-term token used to request a new access token later.
        refresh_token = create_refresh_token(subject=user.id)

        # Return the full login response the frontend will receive.
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role.name,
            },
        }

    def refresh_access_token(self, user: User) -> str:
        """
        Create a brand-new access token for a user who is already validated.

        In simple words:
        if the old short-term token expires, we can make a new one
        without forcing the user to log in again immediately.
        """

        return create_access_token(subject=user.id)