# This file contains the API routes for activities.
# In simple words, this is where the frontend can ask the backend to:
# - show all activities
# - show one activity
# - create a new activity
# - update an existing activity

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# This checks that the user is logged in and active.
from app.core.dependencies import require_active_user

# This gives us a database session/connection.
from app.db.session import get_db

# This is the User model, used for the logged-in user.
from app.models.user import User

# These define the input and output format for activities.
from app.schemas.activity import (
    ActivityCreateRequest,
    ActivityResponse,
    ActivityUpdateRequest,
)

# This contains the activity business logic.
from app.services.activity_service import ActivityService

# All routes in this file will start with /activities
# Example:
# - GET /activities
# - POST /activities
router = APIRouter(prefix="/activities", tags=["Activities"])


@router.get("")
def list_activities(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return all activities.

    In simple words:
    this route gives the logged-in user the full list of activity records.
    """
    # Create the service so we can use the activity logic.
    activity_service = ActivityService(db)

    # Ask the service to get all activities.
    activities = activity_service.list_activities()

    # Return the activities in a clean response format.
    return {
        "success": True,
        "message": "Activities fetched successfully",
        "data": [
            ActivityResponse.model_validate(activity).model_dump()
            for activity in activities
        ],
    }


@router.get("/{activity_id}")
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return one activity by ID.

    In simple words:
    this route gives the details of one specific activity record.
    """
    # Create the service for activity logic.
    activity_service = ActivityService(db)

    try:
        # Ask the service to find the activity by ID.
        activity = activity_service.get_activity(activity_id)

        # If found, return it in a clean response format.
        return {
            "success": True,
            "message": "Activity fetched successfully",
            "data": ActivityResponse.model_validate(activity).model_dump(),
        }
    except ValueError as exc:
        # If the activity does not exist, return a 404 error.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("")
def create_activity(
    payload: ActivityCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Create a new activity.

    In simple words:
    this route adds a new activity record to the CRM.
    """
    # Create the service for activity logic.
    activity_service = ActivityService(db)

    # Ask the service to create the activity using the request data.
    activity = activity_service.create_activity(payload)

    # Return the newly created activity.
    return {
        "success": True,
        "message": "Activity created successfully",
        "data": ActivityResponse.model_validate(activity).model_dump(),
    }


@router.patch("/{activity_id}")
def update_activity(
    activity_id: int,
    payload: ActivityUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Update an activity.

    In simple words:
    this route changes some details of an existing activity record.
    """
    # Create the service for activity logic.
    activity_service = ActivityService(db)

    try:
        # Ask the service to update the activity with the new data.
        activity = activity_service.update_activity(activity_id, payload)

        # Return the updated activity.
        return {
            "success": True,
            "message": "Activity updated successfully",
            "data": ActivityResponse.model_validate(activity).model_dump(),
        }
    except ValueError as exc:
        # If the activity does not exist, return a 404 error.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc