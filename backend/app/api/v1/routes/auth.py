# This file defines the authentication API endpoints.
# In simple words, these are the backend URLs used for:
# - creating a new account
# - logging in
# - getting a new access token
# - logging out
# - checking who is currently logged in

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# This helper finds the currently logged-in user from the access token.
from app.core.dependencies import get_current_user

# This helper reads and checks a refresh token.
from app.core.security import decode_refresh_token

# This gives us a database session so we can read and write data.
from app.db.session import get_db

# This is the User database model.
from app.models.user import User

# This is the database helper for reading users.
from app.repositories.user_repository import UserRepository

# These schemas define the expected input and output shapes for auth-related requests.
from app.schemas.auth import (
    MessageResponse,
    RefreshTokenRequest,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)

# This service contains the main auth business logic.
from app.services.auth_service import AuthService

# Create a router for all auth-related endpoints.
# The final URLs will start with /auth
# Example:
# - /auth/register
# - /auth/login
# - /auth/me
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Create a new user account.

    In simple words:
    the frontend sends registration data here,
    and this route asks the AuthService to create the account.
    """
    # Create the auth service so we can use the registration logic.
    auth_service = AuthService(db)

    try:
        # Ask the service to register the user.
        # The service will:
        # - check if email already exists
        # - check if the role is valid
        # - hash the password
        # - save the user
        user = auth_service.register_user(
            full_name=payload.full_name,
            email=payload.email,
            password=payload.password,
            role_name=payload.role,
        )

        # Return a successful response with the new user's basic info.
        return {
            "success": True,
            "message": "User registered successfully",
            "data": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role.name,
            },
        }
    except ValueError as exc:
        # If registration fails because of invalid input or duplicate email,
        # return a 400 Bad Request error.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/login")
def login_user(
    payload: UserLoginRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Log in a user and return tokens.

    In simple words:
    this endpoint checks the email and password,
    and if they are correct, it gives back login tokens.
    """
    # Create the auth service so we can use the login logic.
    auth_service = AuthService(db)

    try:
        # Check if the email and password are valid.
        user = auth_service.authenticate_user(
            email=payload.email,
            password=payload.password,
        )

        # If login is valid, create the access token + refresh token response.
        token_data = auth_service.create_token_response(user)

        # Return success with token data.
        return {
            "success": True,
            "message": "Login successful",
            "data": token_data,
        }
    except ValueError as exc:
        # If login fails, return 401 Unauthorized.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/refresh")
def refresh_access_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Create a new access token using a refresh token.

    In simple words:
    when the old short-term access token expires,
    the frontend can send the refresh token here
    to ask for a new access token.
    """
    try:
        # Read and validate the refresh token.
        refresh_payload = decode_refresh_token(payload.refresh_token)

        # Get the user ID and token type from the token.
        user_id = refresh_payload.get("sub")
        token_type = refresh_payload.get("type")

        # Make sure this is really a refresh token and has a valid user ID.
        if user_id is None or token_type != "refresh":
            raise ValueError("Invalid refresh token.")

        # Find the user in the database.
        user_repository = UserRepository(db)
        user = user_repository.get_by_id(int(user_id))

        # Reject if the user does not exist or is inactive.
        if user is None or not user.is_active:
            raise ValueError("User not found or inactive.")

        # Create a brand-new access token for the validated user.
        auth_service = AuthService(db)
        new_access_token = auth_service.refresh_access_token(user)

        # Return the new short-term access token.
        return {
            "success": True,
            "message": "Access token refreshed successfully",
            "data": {
                "access_token": new_access_token,
                "token_type": "bearer",
            },
        }
    except ValueError as exc:
        # If the refresh token is bad or the user is invalid,
        # return 401 Unauthorized.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/logout")
def logout_user() -> dict:
    """
    Log out endpoint.

    In simple words:
    for now this only returns a success message.
    It does not truly invalidate tokens yet because
    refresh tokens are not being stored in the database yet.
    """
    return {
        "success": True,
        "message": "Logout successful",
        "data": {},
    }


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)) -> dict:
    """
    Return the currently logged-in user.

    In simple words:
    this endpoint tells the frontend who is currently authenticated,
    based on the access token sent with the request.
    """
    return {
        "success": True,
        "message": "Current user fetched successfully",
        "data": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role.name,
        },
    }