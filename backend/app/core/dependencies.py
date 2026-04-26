# This file contains reusable FastAPI dependencies.
# It is responsible for reading the JWT token, validating it,
# and returning the currently authenticated user.

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

# Clients will send bearer tokens to protected endpoints.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Validate the access token and return the current active user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        token_type = payload.get("type")

        # Make sure the token contains a subject and is an access token.
        if user_id is None or token_type != "access":
            raise credentials_exception

        user_repository = UserRepository(db)
        user = user_repository.get_by_id(int(user_id))

        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise credentials_exception

        return user

    except Exception as exc:
        raise credentials_exception from exc


def require_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Simple alias dependency for routes that require any logged-in active user.
    """
    return current_user