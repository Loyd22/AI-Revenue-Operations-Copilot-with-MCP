"""
Basic tests for MCP server setup.
"""

from app.server import mcp


def test_mcp_server_exists():
    """
    Make sure the MCP server object is created successfully.
    """
    assert mcp is not None