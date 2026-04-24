"""
Policy-related MCP tools.
"""


def register_policy_tools(mcp) -> None:
    """
    Register policy tools to the MCP server.
    """

    @mcp.tool()
    def get_policy_section(section_name: str) -> dict:
        """
        Return placeholder policy text for a named section.
        """
        return {
            "success": True,
            "data": {
                "section_name": section_name,
                "content": "Placeholder policy content for MCP testing.",
            },
        }