from fastapi import APIRouter, Depends

from app.core.dependencies import require_active_user, require_roles
from app.models.user import User

router = APIRouter(prefix="/protected", tags=["Protected"])


@router.get("/profile")
def get_protected_profile(current_user: User = Depends(require_active_user)) -> dict:
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


@router.get("/admin-only")
def get_admin_only_data(
    current_user: User = Depends(require_roles(["admin"])),
) -> dict:
    return {
        "success": True,
        "message": "Admin-only route accessed successfully",
        "data": {
            "user_id": current_user.id,
            "role": current_user.role.name,
            "scope": "admin_only",
        },
    }


@router.get("/leadership")
def get_leadership_data(
    current_user: User = Depends(require_roles(["admin", "sales_director"])),
) -> dict:
    return {
        "success": True,
        "message": "Leadership route accessed successfully",
        "data": {
            "user_id": current_user.id,
            "role": current_user.role.name,
            "scope": "leadership",
        },
    }


@router.get("/ops")
def get_ops_data(
    current_user: User = Depends(require_roles(["admin", "revops_manager"])),
) -> dict:
    return {
        "success": True,
        "message": "Ops route accessed successfully",
        "data": {
            "user_id": current_user.id,
            "role": current_user.role.name,
            "scope": "ops",
        },
    }


@router.get("/revenue-team")
def get_revenue_team_data(
    current_user: User = Depends(
        require_roles(
            [
                "admin",
                "sales_rep",
                "account_manager",
                "revops_manager",
                "sales_director",
            ]
        )
    ),
) -> dict:
    return {
        "success": True,
        "message": "Revenue team route accessed successfully",
        "data": {
            "user_id": current_user.id,
            "role": current_user.role.name,
            "scope": "revenue_team",
        },
    }