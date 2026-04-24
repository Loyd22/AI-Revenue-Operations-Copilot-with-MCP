"""
Main MCP server entry point.

This file creates the MCP server and registers all business tools.
Later, the backend AI workflows will call these tools instead of guessing.
"""

from fastmcp import FastMCP

from app.tools.accounts import register_account_tools
from app.tools.deals import register_deal_tools
from app.tools.activities import register_activity_tools
from app.tools.notes import register_note_tools
from app.tools.pricing import register_pricing_tools
from app.tools.policies import register_policy_tools

# Create the MCP server instance.
mcp = FastMCP("AI Revenue Operations Copilot MCP Server")

# Register tool groups.
register_account_tools(mcp)
register_deal_tools(mcp)
register_activity_tools(mcp)
register_note_tools(mcp)
register_pricing_tools(mcp)
register_policy_tools(mcp)

if __name__ == "__main__":
    mcp.run()