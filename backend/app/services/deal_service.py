# This file handles the business rules for deals.
# In simple words, it decides:
# - how to get deals
# - what to do if a deal is missing
# - how to create a new deal safely
# - how to update a deal safely
#
# It does not directly handle raw database queries.
# That part is done by the repository.

from sqlalchemy.orm import Session

from app.models.deal import Deal
from app.repositories.deal_repository import DealRepository
from app.schemas.deal import DealCreateRequest, DealUpdateRequest


class DealService:
    """
    Business logic for deal actions.
    """

    def __init__(self, db: Session):
        # Use the deal repository for database work
        self.deal_repository = DealRepository(db)

    def list_deals(self) -> list[Deal]:
        # Return all deals
        return self.deal_repository.get_all()

    def get_deal(self, deal_id: int) -> Deal:
        # Find one deal by ID
        # If it does not exist, return an error
        deal = self.deal_repository.get_by_id(deal_id)
        if deal is None:
            raise ValueError("Deal not found.")
        return deal

    def create_deal(self, payload: DealCreateRequest) -> Deal:
        # Check if another deal already has the same title
        existing_deal = self.deal_repository.get_by_title(payload.title)
        if existing_deal is not None:
            raise ValueError("A deal with this title already exists.")

        # Create a new Deal object from the request data
        deal = Deal(
            account_id=payload.account_id,
            owner_user_id=payload.owner_user_id,
            stage_id=payload.stage_id,
            title=payload.title,
            amount=payload.amount,
            status=payload.status,
            risk_level=payload.risk_level,
            expected_close_date=payload.expected_close_date,
            last_activity_at=payload.last_activity_at,
        )

        # Save the new deal using the repository
        return self.deal_repository.create(deal)

    def update_deal(self, deal_id: int, payload: DealUpdateRequest) -> Deal:
        # Find the deal first
        deal = self.deal_repository.get_by_id(deal_id)
        if deal is None:
            raise ValueError("Deal not found.")

        # Get only the fields that were actually sent in the update request
        update_data = payload.model_dump(exclude_unset=True)

        # If the title is changing, make sure the new title is still unique
        if "title" in update_data and update_data["title"] != deal.title:
            existing_deal = self.deal_repository.get_by_title(update_data["title"])
            if existing_deal is not None:
                raise ValueError("A deal with this title already exists.")

        # Apply each updated field to the deal object
        for field, value in update_data.items():
            setattr(deal, field, value)

        # Save the updated deal
        return self.deal_repository.update(deal)