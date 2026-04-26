# This file contains sample protected routes.
# We use it to prove that JWT validation works correctly in FastAPI.

from fastapi import APIRouter, Depends

from app.core.dependencies import require_active_user
from app.models.user import User

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/profile")
def get_protected_profile(current_user: User = Depends(require_active_user)) -> dict:
    """
    Example protected route that returns the logged-in user's profile.
    """
    return {
        "success": True,
        "message": "Protected profile fetched successfully",
        "data": {
            "id": current_user.id,
            "full_name": current_user.full_name,
            "email": current_user.email,
            "role": current_user.role.name,
            "is_active": current_user.is_active,
        },
    }