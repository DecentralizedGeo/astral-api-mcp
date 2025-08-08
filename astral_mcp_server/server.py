"""
Astral MCP Server

A FastMCP-based server that provides tools for querying location attestations
through the Astral API.
"""

import asyncio
import logging
from typing import Any, Dict

import httpx
from mcp.server.fastmcp import FastMCP

# Import from absolute paths when running as script
try:
    from .config import (
        ASTRAL_HEALTH_ENDPOINT,
        DEFAULT_TIMEOUT,
        MAX_RETRIES,
        SERVER_NAME,
        SERVER_VERSION,
        get_api_key,
    )
except ImportError:
    # Fallback for when running as script
    from config import (
        ASTRAL_HEALTH_ENDPOINT,
        DEFAULT_TIMEOUT,
        MAX_RETRIES,
        SERVER_NAME,
        SERVER_VERSION,
        get_api_key,
    )

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
app = FastMCP(SERVER_NAME)


@app.tool()
async def check_astral_api_health() -> Dict[str, Any]:
    """
    Check the health status of the Astral API.
    
    Performs a health check against the Astral API endpoint to verify
    connectivity and service availability.
    
    Returns:
        Dict[str, Any]: Health check response containing status information
        
    Raises:
        Exception: If the health check fails or times out
    """
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            logger.info(f"Checking Astral API health at: {ASTRAL_HEALTH_ENDPOINT}")
            
            response = await client.get(ASTRAL_HEALTH_ENDPOINT)
            response.raise_for_status()
            
            health_data = response.json()
            
            result = {
                "status": "healthy",
                "endpoint": ASTRAL_HEALTH_ENDPOINT,
                "response_code": response.status_code,
                "response_time_ms": int(response.elapsed.total_seconds() * 1000),
                "api_data": health_data,
            }
            
            logger.info(f"Health check successful: {result['status']}")
            return result
            
    except httpx.TimeoutException:
        error_msg = f"Health check timed out after {DEFAULT_TIMEOUT} seconds"
        logger.error(error_msg)
        raise Exception(error_msg)
        
    except httpx.HTTPStatusError as e:
        error_msg = f"Health check failed with status {e.response.status_code}: {e.response.text}"
        logger.error(error_msg)
        raise Exception(error_msg)
        
    except Exception as e:
        error_msg = f"Health check failed: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)


@app.tool()
async def get_server_info() -> Dict[str, Any]:
    """
    Get information about this MCP server.
    
    Returns basic metadata and configuration information about the
    Astral MCP server instance.
    
    Returns:
        Dict[str, Any]: Server information including name, version, and capabilities
    """
    api_key_configured = get_api_key() is not None
    
    return {
        "name": SERVER_NAME,
        "version": SERVER_VERSION,
        "description": "MCP server for querying Astral location attestations",
        "api_key_configured": api_key_configured,
        "astral_health_endpoint": ASTRAL_HEALTH_ENDPOINT,
        "capabilities": [
            "health_check",
            "server_info",
        ],
    }


def main() -> None:
    """
    Main entry point for running the MCP server.
    
    This function starts the FastMCP server and handles the event loop.
    """
    logger.info(f"Starting {SERVER_NAME} v{SERVER_VERSION}")
    
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()