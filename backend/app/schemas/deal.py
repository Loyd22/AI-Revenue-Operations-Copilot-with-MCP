# These schemas describe the data format for deals.
# In simple words, they define:
# - what data is needed when creating a deal
# - what data can be changed when updating a deal
# - what data will be returned to the frontend

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class DealBase(BaseModel):
    # Shared fields used for deal data
    account_id: int
    owner_user_id: int | None = None
    stage_id: int | None = None
    title: str
    amount: Decimal | None = None
    status: str = "open"
    risk_level: str | None = None
    expected_close_date: date | None = None
    last_activity_at: datetime | None = None


class DealCreateRequest(DealBase):
    # Request body for creating a new deal
    # It uses all fields from DealBase
    pass


class DealUpdateRequest(BaseModel):
    # Request body for updating an existing deal
    # All fields are optional because partial update is allowed
    account_id: int | None = None
    owner_user_id: int | None = None
    stage_id: int | None = None
    title: str | None = None
    amount: Decimal | None = None
    status: str | None = None
    risk_level: str | None = None
    expected_close_date: date | None = None
    last_activity_at: datetime | None = None


class DealResponse(BaseModel):
    # Response model for returning deal data to the frontend
    id: int
    account_id: int
    owner_user_id: int | None
    stage_id: int | None
    title: str
    amount: Decimal | None
    status: str
    risk_level: str | None
    expected_close_date: date | None
    last_activity_at: datetime | None

    # This allows Pydantic to read data directly from SQLAlchemy model objects
    model_config = {"from_attributes": True}