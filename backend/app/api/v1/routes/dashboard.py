# This file contains the dashboard API route.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import require_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    dashboard_service = DashboardService(db)
    dashboard_data = dashboard_service.get_dashboard_data()

    validated = DashboardResponse.model_validate(dashboard_data)

    return {
        "success": True,
        "message": "Dashboard data fetched successfully",
        "data": validated.model_dump(),
    }