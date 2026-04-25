# This file contains reusable helper functions for FastAPI routes.
# The main job here is to figure out who the currently logged-in user is
# by reading the login token sent by the frontend.

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# This function reads and checks the access token.
from app.core.security import decode_access_token

# This gives us a database session so we can read user data.
from app.db.session import get_db

# This is the User database model.
from app.models.user import User

# This is the database helper for finding users.
from app.repositories.user_repository import UserRepository

# This tells FastAPI that protected routes expect a bearer token.
# In simple words:
# when a user is already logged in, the frontend sends the token
# in the Authorization header, and FastAPI gets it from here.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Find and return the currently logged-in user.

    In simple words, this function does these steps:
    1. Read the token sent by the frontend
    2. Decode the token to see who the user is
    3. Check that it is really an access token
    4. Look up that user in the database
    5. Make sure the user still exists and is active
    6. Return that user object
    """

    # This is the standard error we return if the token is invalid
    # or the user cannot be trusted.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )

    try:
        # Decode the token so we can read the data inside it.
        # Usually this includes the user ID and the token type.
        payload = decode_access_token(token)

        # "sub" usually means the user ID stored inside the token.
        user_id = payload.get("sub")

        # "type" tells us what kind of token this is.
        # We expect it to be an access token here.
        token_type = payload.get("type")

        # If there is no user ID, or if the token is not an access token,
        # we reject it.
        if user_id is None or token_type != "access":
            raise credentials_exception

        # Create the repository so we can find the user in the database.
        user_repository = UserRepository(db)

        # Get the user by ID from the database.
        user = user_repository.get_by_id(int(user_id))

        # If the user does not exist anymore, or the account is inactive,
        # reject the request.
        if user is None or not user.is_active:
            raise credentials_exception

        # If everything is valid, return the logged-in user.
        return user

    except Exception as exc:
        # If anything goes wrong during token reading or user lookup,
        # return the same authentication error.
        raise credentials_exception from exc