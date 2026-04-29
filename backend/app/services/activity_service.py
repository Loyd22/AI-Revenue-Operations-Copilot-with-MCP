# This file handles the business rules for activities.
# In simple words, it decides:
# - how to get activities
# - what to do if an activity is missing
# - how to create a new activity
# - how to update an activity
#
# It does not directly do raw database queries.
# That part is handled by the repository.

from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.repositories.activity_repository import ActivityRepository
from app.schemas.activity import ActivityCreateRequest, ActivityUpdateRequest


class ActivityService:
    """
    Business logic for activity actions.
    """

    def __init__(self, db: Session):
        # Use the activity repository for database work
        self.activity_repository = ActivityRepository(db)

    def list_activities(self) -> list[Activity]:
        # Return all activities
        return self.activity_repository.get_all()

    def get_activity(self, activity_id: int) -> Activity:
        # Find one activity by ID
        # If it does not exist, return an error
        activity = self.activity_repository.get_by_id(activity_id)
        if activity is None:
            raise ValueError("Activity not found.")
        return activity

    def create_activity(self, payload: ActivityCreateRequest) -> Activity:
        # Create a new Activity object from the request data
        activity = Activity(
            account_id=payload.account_id,
            deal_id=payload.deal_id,
            user_id=payload.user_id,
            activity_type=payload.activity_type,
            subject=payload.subject,
            activity_at=payload.activity_at,
            status=payload.status,
            summary=payload.summary,
        )

        # Save the new activity using the repository
        return self.activity_repository.create(activity)

    def update_activity(self, activity_id: int, payload: ActivityUpdateRequest) -> Activity:
        # Find the activity first
        activity = self.activity_repository.get_by_id(activity_id)
        if activity is None:
            raise ValueError("Activity not found.")

        # Get only the fields that were actually sent in the update request
        update_data = payload.model_dump(exclude_unset=True)

        # Apply each updated field to the activity object
        for field, value in update_data.items():
            setattr(activity, field, value)

        # Save the updated activity
        return self.activity_repository.update(activity)