"""
Account-related MCP tools.
"""

from app.auth.permissions import can_view_account


def register_account_tools(mcp) -> None:
    """
    Register account tools to the MCP server.
    """

    @mcp.tool()
    def get_account(account_id: int, user_role: str = "sales_rep") -> dict:
        """
        Return one account record.

        This is placeholder data for now.
        Later, this should read from the real database.
        """
        if not can_view_account(user_role):
            return {
                "success": False,
                "error": "FORBIDDEN",
                "message": "You do not have permission to view account data.",
            }

        return {
            "success": True,
            "data": {
                "id": account_id,
                "name": "Acme Growth Co",
                "industry": "SaaS",
                "company_size": "SMB",
                "status": "active",
                "health_status": "healthy",
            },
        } 