# This file contains the API routes for deals.
# In simple words, this is where the frontend can ask the backend to:
# - show all deals
# - show one deal
# - create a new deal
# - update an existing deal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

# This checks that the user is logged in and active.
from app.core.dependencies import require_active_user

# This gives us a database session/connection.
from app.db.session import get_db

# This is the User model, used for the logged-in user.
from app.models.user import User

# These define the input and output format for deals.
from app.schemas.deal import DealCreateRequest, DealResponse, DealUpdateRequest

# This contains the deal business logic.
from app.services.deal_service import DealService

# All routes in this file will start with /deals
# Example:
# - GET /deals
# - POST /deals
router = APIRouter(prefix="/deals", tags=["Deals"])


@router.get("")
def list_deals(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return all deals.

    In simple words:
    this route gives the logged-in user the full list of deals.
    """
    # Create the service so we can use the deal logic.
    deal_service = DealService(db)

    # Ask the service to get all deals.
    deals = deal_service.list_deals()

    # Return the deals in a clean response format.
    return {
        "success": True,
        "message": "Deals fetched successfully",
        "data": [DealResponse.model_validate(deal).model_dump() for deal in deals],
    }


@router.get("/{deal_id}")
def get_deal(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Return one deal by ID.

    In simple words:
    this route gives the details of one specific deal.
    """
    # Create the service for deal logic.
    deal_service = DealService(db)

    try:
        # Ask the service to find the deal by ID.
        deal = deal_service.get_deal(deal_id)

        # If found, return it in a clean response format.
        return {
            "success": True,
            "message": "Deal fetched successfully",
            "data": DealResponse.model_validate(deal).model_dump(),
        }
    except ValueError as exc:
        # If the deal does not exist, return a 404 error.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post("")
def create_deal(
    payload: DealCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Create a new deal.

    In simple words:
    this route adds a new deal to the CRM.
    """
    # Create the service for deal logic.
    deal_service = DealService(db)

    try:
        # Ask the service to create the deal using the request data.
        deal = deal_service.create_deal(payload)

        # Return the newly created deal.
        return {
            "success": True,
            "message": "Deal created successfully",
            "data": DealResponse.model_validate(deal).model_dump(),
        }
    except ValueError as exc:
        # If something is wrong, like duplicate deal title,
        # return a 400 Bad Request error.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.patch("/{deal_id}")
def update_deal(
    deal_id: int,
    payload: DealUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_active_user),
) -> dict:
    """
    Update a deal.

    In simple words:
    this route changes some details of an existing deal.
    """
    # Create the service for deal logic.
    deal_service = DealService(db)

    try:
        # Ask the service to update the deal with the new data.
        deal = deal_service.update_deal(deal_id, payload)

        # Return the updated deal.
        return {
            "success": True,
            "message": "Deal updated successfully",
            "data": DealResponse.model_validate(deal).model_dump(),
        }
    except ValueError as exc:
        # Decide which error code to return:
        # - 404 if the deal does not exist
        # - 400 for other problems like duplicate deal title
        message = str(exc)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if message == "Deal not found."
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(
            status_code=status_code,
            detail=message,
        ) from exc