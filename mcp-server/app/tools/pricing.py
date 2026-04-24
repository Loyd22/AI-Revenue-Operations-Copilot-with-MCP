"""
Pricing-related MCP tools.
"""

from app.auth.permissions import can_view_pricing


def register_pricing_tools(mcp) -> None:
    """
    Register pricing tools to the MCP server.
    """

    @mcp.tool()
    def get_pricing_rules(user_role: str = "sales_rep") -> dict:
        """
        Return placeholder pricing guidance.
        """
        if not can_view_pricing(user_role):
            return {
                "success": False,
                "error": "FORBIDDEN",
                "message": "You do not have permission to view pricing rules.",
            }

        return {
            "success": True,
            "data": {
                "standard_discount_limit_percent": 10,
                "director_approval_required_above_percent": 10,
            },
        }