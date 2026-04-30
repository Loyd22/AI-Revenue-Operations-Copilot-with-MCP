# These schemas define the response shape for the dashboard API.

from pydantic import BaseModel


class DashboardMetricItem(BaseModel):
    label: str
    value: int


class DashboardRecentAccountItem(BaseModel):
    id: int
    name: str
    industry: str | None
    status: str
    health_status: str | None

    model_config = {"from_attributes": True}


class DashboardRecentDealItem(BaseModel):
    id: int
    title: str
    status: str
    risk_level: str | None
    account_id: int

    model_config = {"from_attributes": True}


class DashboardRecentActivityItem(BaseModel):
    id: int
    subject: str
    activity_type: str
    status: str
    account_id: int

    model_config = {"from_attributes": True}


class DashboardRecentNoteItem(BaseModel):
    id: int
    note_type: str
    content: str
    account_id: int

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    total_accounts: int
    total_deals: int
    total_activities: int
    total_notes: int
    deals_by_risk: list[DashboardMetricItem]
    deals_by_status: list[DashboardMetricItem]
    recent_accounts: list[DashboardRecentAccountItem]
    recent_deals: list[DashboardRecentDealItem]
    recent_activities: list[DashboardRecentActivityItem]
    recent_notes: list[DashboardRecentNoteItem]