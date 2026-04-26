# This file contains reusable FastAPI dependencies.
# It validates JWT tokens, returns the current user,
# and provides role-based access control helpers.

from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

# Swagger-compatible token endpoint for OAuth2 password flow.
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

        if user_id is None or token_type != "access":
            raise credentials_exception

        user_repository = UserRepository(db)
        user = user_repository.get_by_id(int(user_id))

        if user is None or not user.is_active:
            raise credentials_exception

        return user

    except Exception as exc:
        raise credentials_exception from exc


def require_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Simple alias for routes that require any logged-in active user.
    """
    return current_user


def require_roles(allowed_roles: list[str]) -> Callable:
    """
    Factory that returns a dependency function for checking allowed roles.

    Example:
        Depends(require_roles(["admin"]))
        Depends(require_roles(["admin", "sales_director"]))
    """

    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        user_role = current_user.role.name

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource.",
            )

        return current_user

    return role_checker