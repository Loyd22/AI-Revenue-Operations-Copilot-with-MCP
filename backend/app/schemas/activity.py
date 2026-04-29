# These schemas define the input and output shapes for activities.

from datetime import datetime

from pydantic import BaseModel


class ActivityBase(BaseModel):
    account_id: int
    deal_id: int | None = None
    user_id: int | None = None
    activity_type: str
    subject: str
    activity_at: datetime
    status: str = "completed"
    summary: str | None = None


class ActivityCreateRequest(ActivityBase):
    pass


class ActivityUpdateRequest(BaseModel):
    account_id: int | None = None
    deal_id: int | None = None
    user_id: int | None = None
    activity_type: str | None = None
    subject: str | None = None
    activity_at: datetime | None = None
    status: str | None = None
    summary: str | None = None


class ActivityResponse(BaseModel):
    id: int
    account_id: int
    deal_id: int | None
    user_id: int | None
    activity_type: str
    subject: str
    activity_at: datetime
    status: str
    summary: str | None

    model_config = {"from_attributes": True}