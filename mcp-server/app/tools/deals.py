"""
Deal-related MCP tools.
"""


def register_deal_tools(mcp) -> None:
    """
    Register deal tools to the MCP server.
    """

    @mcp.tool()
    def get_deal(deal_id: int) -> dict:
        """
        Return one deal record.

        This is placeholder data for now.
        """
        return {
            "success": True,
            "data": {
                "id": deal_id,
                "title": "Renewal Opportunity",
                "amount": 12000,
                "stage": "proposal",
                "risk_level": "medium",
            },
        }