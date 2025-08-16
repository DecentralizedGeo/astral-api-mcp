"""
Tests for the Astral MCP Server
"""

import pytest

from astral_mcp_server import __version__


def test_version() -> None:
    """Test that version is properly defined."""
    assert __version__ == "0.1.0"


def test_import() -> None:
    """Test that the main module can be imported."""
    import astral_mcp_server
    assert hasattr(astral_mcp_server, "app")


@pytest.mark.asyncio
async def test_server_info_tool() -> None:
    """Test the server info tool."""
    from astral_mcp_server.server import get_server_info

    info = await get_server_info()

    assert info["name"] == "astral-mcp-server"
    assert info["version"] == "0.1.0"
    assert "capabilities" in info
    assert isinstance(info["capabilities"], list)

    # Check that new tools are listed in capabilities
    expected_capabilities = [
        "health_check",
        "server_info",
        "query_location_proofs",
        "get_location_proof_by_uid",
        "get_astral_config",
    ]
    for capability in expected_capabilities:
        assert capability in info["capabilities"]


@pytest.mark.asyncio
async def test_query_location_proofs_validation() -> None:
    """Test input validation for query_location_proofs tool."""
    from astral_mcp_server.server import query_location_proofs

    # Test invalid limit
    result = await query_location_proofs(limit=0)
    assert result["success"] is False
    assert result["error"] == "validation_error"

    # Test invalid prover address
    result = await query_location_proofs(prover="invalid_address")
    assert result["success"] is False
    assert result["error"] == "validation_error"

    # Test negative offset
    result = await query_location_proofs(offset=-1)
    assert result["success"] is False
    assert result["error"] == "validation_error"


@pytest.mark.asyncio
async def test_get_location_proof_by_uid_validation() -> None:
    """Test input validation for get_location_proof_by_uid tool."""
    from astral_mcp_server.server import get_location_proof_by_uid

    # Test invalid UID format
    result = await get_location_proof_by_uid("invalid_uid")
    assert result["success"] is False
    assert result["error"] == "validation_error"

    # Test short UID
    result = await get_location_proof_by_uid("0x123")
    assert result["success"] is False
    assert result["error"] == "validation_error"

    # Test with valid UID from EAS (but does not exist in AstralAPI backend)
    result = await get_location_proof_by_uid(
        "0x8eb2b2105f9c8828b97966a23c001fdec38c7b02c98ce73969edcda50bad474a"
    )
    assert result["success"] is False
    assert result["error"] == "not_found"

    # test with valid UID that exists in AstralAPI backend
    # Should return a `success` response with data
    result = await get_location_proof_by_uid(
        "0x46268c50ec0a2962319273ccb37bd5c50a7ee24e34b06313162d9769cea18b3f"
    )
    assert result["success"] is True
    assert result["data"] is not None
    assert "error" not in result
    assert (
        result["data"]["uid"]
        == "0x46268c50ec0a2962319273ccb37bd5c50a7ee24e34b06313162d9769cea18b3f"
    )
