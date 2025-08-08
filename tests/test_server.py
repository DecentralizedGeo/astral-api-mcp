"""
Tests for the Astral MCP Server
"""

import pytest
from astral_mcp_server import __version__


def test_version():
    """Test that version is properly defined."""
    assert __version__ == "0.1.0"


def test_import():
    """Test that the main module can be imported."""
    import astral_mcp_server
    assert hasattr(astral_mcp_server, "app")


@pytest.mark.asyncio
async def test_server_info_tool():
    """Test the server info tool."""
    from astral_mcp_server.server import get_server_info
    
    info = await get_server_info()
    
    assert info["name"] == "astral-mcp-server"
    assert info["version"] == "0.1.0"
    assert "capabilities" in info
    assert isinstance(info["capabilities"], list)