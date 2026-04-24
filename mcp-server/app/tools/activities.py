"""
Activity-related MCP tools.
"""


def register_activity_tools(mcp) -> None:
    """
    Register activity tools to the MCP server.
    """

    @mcp.tool()
    def get_recent_activities(account_id: int) -> dict:
        """
        Return placeholder recent activities for an account.
        """
        return {
            "success": True,
            "data": [
                {
                    "id": 1,
                    "account_id": account_id,
                    "activity_type": "meeting",
                    "subject": "Pricing review",
                },
                {
                    "id": 2,
                    "account_id": account_id,
                    "activity_type": "email",
                    "subject": "Sent follow-up summary",
                },
            ],
        }