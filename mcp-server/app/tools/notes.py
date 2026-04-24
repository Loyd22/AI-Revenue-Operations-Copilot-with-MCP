"""
Note-related MCP tools.
"""


def register_note_tools(mcp) -> None:
    """
    Register note tools to the MCP server.
    """

    @mcp.tool()
    def get_notes(account_id: int) -> dict:
        """
        Return placeholder notes for an account.
        """
        return {
            "success": True,
            "data": [
                {
                    "id": 1,
                    "account_id": account_id,
                    "note_type": "meeting_note",
                    "content": "Customer asked about discount flexibility.",
                }
            ],
        }