# These schemas define the input and output structure
# for the accounts API.

from datetime import date

from pydantic import BaseModel


class AccountBase(BaseModel):
    """
    Shared account fields.
    """
    name: str
    industry: str | None = None
    company_size: str | None = None
    status: str = "active"
    health_status: str | None = None
    renewal_date: date | None = None
    owner_user_id: int | None = None


class AccountCreateRequest(AccountBase):
    """
    Request body for creating a new account.
    """
    pass


class AccountUpdateRequest(BaseModel):
    """
    Request body for updating an account.
    All fields are optional for partial updates.
    """
    name: str | None = None
    industry: str | None = None
    company_size: str | None = None
    status: str | None = None
    health_status: str | None = None
    renewal_date: date | None = None
    owner_user_id: int | None = None


class AccountResponse(BaseModel):
    """
    Response model for returning account data.
    """
    id: int
    name: str
    industry: str | None
    company_size: str | None
    status: str
    health_status: str | None
    renewal_date: date | None
    owner_user_id: int | None

    model_config = {"from_attributes": True}