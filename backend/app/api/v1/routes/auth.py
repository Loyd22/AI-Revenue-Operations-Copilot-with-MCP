# This file contains the auth API routes:
# register, login, token, refresh, logout, and current user.

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import decode_refresh_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    RefreshTokenRequest,
    UserLoginRequest,
    UserRegisterRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(
    payload: UserRegisterRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Register a new user.
    """
    auth_service = AuthService(db)

    try:
        user = auth_service.register_user(
            full_name=payload.full_name,
            email=payload.email,
            password=payload.password,
            role_name=payload.role,
        )
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
    Frontend login endpoint using JSON body.
    """
    auth_service = AuthService(db)

    try:
        user = auth_service.authenticate_user(
            email=payload.email,
            password=payload.password,
        )
        token_data = auth_service.create_token_response(user)

        return {
            "success": True,
            "message": "Login successful",
            "data": token_data,
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/token")
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    """
    Swagger-compatible OAuth2 password flow endpoint.

    Swagger sends 'username' and 'password'.
    In this project, we treat 'username' as the user's email.
    This route returns the standard OAuth2 token shape.
    """
    auth_service = AuthService(db)

    try:
        user = auth_service.authenticate_user(
            email=form_data.username,
            password=form_data.password,
        )
        token_data = auth_service.create_token_response(user)

        return {
            "access_token": token_data["access_token"],
            "token_type": "bearer",
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


@router.post("/refresh")
def refresh_access_token(
    payload: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> dict:
    """
    Create a new access token using a refresh token.
    """
    try:
        refresh_payload = decode_refresh_token(payload.refresh_token)
        user_id = refresh_payload.get("sub")
        token_type = refresh_payload.get("type")

        if user_id is None or token_type != "refresh":
            raise ValueError("Invalid refresh token.")

        user_repository = UserRepository(db)
        user = user_repository.get_by_id(int(user_id))

        if user is None or not user.is_active:
            raise ValueError("User not found or inactive.")

        auth_service = AuthService(db)
        new_access_token = auth_service.refresh_access_token(user)

        return {
            "success": True,
            "message": "Access token refreshed successfully",
            "data": {
                "access_token": new_access_token,
                "token_type": "bearer",
            },
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/logout")
def logout_user() -> dict:
    """
    Placeholder logout endpoint.
    """
    return {
        "success": True,
        "message": "Logout successful",
        "data": {},
    }


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)) -> dict:
    """
    Return the currently authenticated user.
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