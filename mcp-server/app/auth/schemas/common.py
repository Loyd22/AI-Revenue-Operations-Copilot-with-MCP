"""
Shared MCP schemas.

These models keep tool input/output structured and predictable.
"""

from pydantic import BaseModel


class ToolContext(BaseModel):
    """
    Basic context passed to tools.

    Later, this can include:
    - user_id
    - role
    - org/team scope
    - request_id
    """
    user_id: int
    user_role: str


class AccountLookupInput(BaseModel):
    """
    Input schema for fetching one account.
    """
    account_id: int


class DealLookupInput(BaseModel):
    """
    Input schema for fetching one deal.
    """
    deal_id: int