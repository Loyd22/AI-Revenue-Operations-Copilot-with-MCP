"""
Simple permission helpers for MCP tools.

For now, this is only a placeholder.
Later, this should check role, ownership, and access scope.
"""


def can_view_account(user_role: str) -> bool:
    """
    Return True if the role is allowed to view account data.
    """
    allowed_roles = {
        "admin",
        "sales_rep",
        "account_manager",
        "revops_manager",
        "sales_director",
    }
    return user_role in allowed_roles


def can_view_pricing(user_role: str) -> bool:
    """
    Example permission check for pricing-related tools.
    """
    allowed_roles = {
        "admin",
        "sales_rep",
        "account_manager",
        "revops_manager",
        "sales_director",
    }
    return user_role in allowed_roles