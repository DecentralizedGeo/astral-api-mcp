"""
Astral MCP Server

A FastMCP-based server that provides tools for querying location attestations
through the Astral API.
"""

import asyncio
import logging
import re
from typing import Any, Dict, List, Optional, Union

import httpx
from mcp.server.fastmcp import FastMCP

# Import from absolute paths when running as script
try:
    from .config import (
        ASTRAL_HEALTH_ENDPOINT,
        ASTRAL_LOCATION_PROOFS_ENDPOINT,
        ASTRAL_CONFIG_ENDPOINT,
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
        ASTRAL_LOCATION_PROOFS_ENDPOINT,
        ASTRAL_CONFIG_ENDPOINT,
        DEFAULT_TIMEOUT,
        MAX_RETRIES,
        SERVER_NAME,
        SERVER_VERSION,
        get_api_key,
    )

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


### CONSTANTS
"""Max length for error text in API responses to prevent excessive output."""
ERROR_TEXT_TRUNCATE_LENGTH = 500


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
                "response_time_ms": (
                    int(response.elapsed.total_seconds() * 1000)
                    if response.elapsed is not None
                    else None
                ),
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
            "query_location_proofs",
            "get_location_proof_by_uid",
            "get_astral_config",
        ],
    }


@app.tool()
async def query_location_proofs(
    chain: Optional[str] = None,
    prover: Optional[str] = None,
    limit: Optional[int] = 10,
    offset: Optional[int] = 0
) -> Dict[str, Any]:
    """
    Query location proofs (attestations) from the Astral API with filtering capabilities.
    
    Enables searching for location attestations using chain, prover, and limit filters
    to analyze blockchain location activity and identify patterns in attestation data.
    
    Args:
        chain (Optional[str]): Filter by blockchain network (e.g., "ethereum", "polygon")
        prover (Optional[str]): Filter by prover address (hexadecimal address)
        limit (Optional[int]): Maximum number of results to return (default: 10, max: 100)
        offset (Optional[int]): Number of results to skip for pagination (default: 0)
    
    Returns:
        Dict[str, Any]: Response containing location proofs array and metadata
        
    Raises:
        Exception: If the API request fails or parameters are invalid
    """
    try:
        # Input validation
        if limit is not None:
            if not isinstance(limit, int) or limit < 1 or limit > 100:
                raise ValueError("limit must be an integer between 1 and 100")
        
        if offset is not None:
            if not isinstance(offset, int) or offset < 0:
                raise ValueError("offset must be a non-negative integer")
                
        if prover is not None:
            # Basic hex address validation
            if not re.match(r'^0x[a-fA-F0-9]{40}$', prover):
                raise ValueError("prover must be a valid 40-character hexadecimal address starting with 0x")
        
        # Build query parameters
        params = {}
        if chain is not None:
            params["chain"] = chain
        if prover is not None:
            params["prover"] = prover
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
            
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            logger.info(f"Querying location proofs with params: {params}")
            
            response = await client.get(ASTRAL_LOCATION_PROOFS_ENDPOINT, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                "success": True,
                "data": data,
                "query_params": params,
                "response_code": response.status_code,
                "response_time_ms": (
                    int(response.elapsed.total_seconds() * 1000)
                    if response.elapsed is not None
                    else None
                ),
            }
            
            logger.info(f"Successfully retrieved {len(data.get('location_proofs', []))} location proofs")
            return result
            
    except ValueError as e:
        error_msg = f"Invalid parameter: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": "validation_error",
            "message": error_msg,
            "details": {"parameter_validation": str(e)}
        }
        
    except httpx.TimeoutException:
        error_msg = f"Request timed out after {DEFAULT_TIMEOUT} seconds"
        logger.error(error_msg)
        return {
            "success": False,
            "error": "timeout_error",
            "message": error_msg,
            "details": {"timeout_seconds": DEFAULT_TIMEOUT}
        }
        
    except httpx.HTTPStatusError as e:
        error_msg = f"API request failed with status {e.response.status_code}"
        logger.error(f"{error_msg}: {e.response.text}")
        return {
            "success": False,
            "error": "api_error",
            "message": error_msg,
            "details": {
                "status_code": e.response.status_code,
                "response_text": e.response.text[:ERROR_TEXT_TRUNCATE_LENGTH],
            },
        }
        
    except Exception as e:
        error_msg = f"Unexpected error querying location proofs: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": "unexpected_error",
            "message": error_msg,
            "details": {"exception_type": type(e).__name__}
        }


@app.tool()
async def get_location_proof_by_uid(uid: str) -> Dict[str, Any]:
    """
    Retrieve a specific location proof attestation by its unique identifier.
    
    Enables fetching complete attestation details including raw attestation content,
    decoded fields, and verification evidence for detailed analysis.
    
    Args:
        uid (str): Unique identifier for the location proof (66-character hex string starting with 0x)
        
    Returns:
        Dict[str, Any]: Complete location proof data or structured error response
        
    Raises:
        Exception: If the UID format is invalid or API request fails
    """
    try:
        # Validate UID format
        if not isinstance(uid, str):
            raise ValueError("uid must be a string")
            
        if not re.match(r'^0x[a-fA-F0-9]{64}$', uid):
            raise ValueError("uid must be a 66-character hexadecimal string starting with 0x")
            
        endpoint = f"{ASTRAL_LOCATION_PROOFS_ENDPOINT}/{uid}"
        
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            logger.info(f"Fetching location proof with UID: {uid}")
            
            response = await client.get(endpoint)
            
            if response.status_code == 404:
                return {
                    "success": False,
                    "error": "not_found",
                    "message": f"Location proof not found for UID: {uid}",
                    "details": {"attempted_uid": uid}
                }
                
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                "success": True,
                "data": data,
                "uid": uid,
                "response_code": response.status_code,
                "response_time_ms": (
                    int(response.elapsed.total_seconds() * 1000)
                    if response.elapsed is not None
                    else None
                ),
            }
            
            logger.info(f"Successfully retrieved location proof for UID: {uid}")
            return result
            
    except ValueError as e:
        error_msg = f"Invalid UID format: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": "validation_error", 
            "message": error_msg,
            "details": {"attempted_uid": uid, "format_requirement": "66-character hex string starting with 0x"}
        }
        
    except httpx.TimeoutException:
        error_msg = f"Request timed out after {DEFAULT_TIMEOUT} seconds"
        logger.error(error_msg)
        return {
            "success": False,
            "error": "timeout_error",
            "message": error_msg,
            "details": {"attempted_uid": uid, "timeout_seconds": DEFAULT_TIMEOUT}
        }
        
    except httpx.HTTPStatusError as e:
        error_msg = f"API request failed with status {e.response.status_code}"
        logger.error(f"{error_msg}: {e.response.text}")
        return {
            "success": False,
            "error": "api_error", 
            "message": error_msg,
            "details": {
                "attempted_uid": uid,
                "status_code": e.response.status_code,
                "response_text": e.response.text[:ERROR_TEXT_TRUNCATE_LENGTH],
            },
        }
        
    except Exception as e:
        error_msg = f"Unexpected error fetching location proof: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": "unexpected_error",
            "message": error_msg,
            "details": {"attempted_uid": uid, "exception_type": type(e).__name__}
        }


@app.tool()
async def get_astral_config() -> Dict[str, Any]:
    """
    Get Astral API configuration information including supported chains and schemas.
    
    Provides configuration data to help users understand which chains, schemas, and 
    capabilities are supported by the Astral API for making informed queries.
    
    Returns:
        Dict[str, Any]: Configuration data including chains, schemas, and API capabilities
        
    Raises:
        Exception: If the configuration endpoint is unavailable
    """
    try:
        async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
            logger.info(f"Fetching Astral API configuration from: {ASTRAL_CONFIG_ENDPOINT}")
            
            response = await client.get(ASTRAL_CONFIG_ENDPOINT)
            response.raise_for_status()
            
            config_data = response.json()
            
            result = {
                "success": True,
                "data": config_data,
                "endpoint": ASTRAL_CONFIG_ENDPOINT,
                "response_code": response.status_code,
                "response_time_ms": (
                    int(response.elapsed.total_seconds() * 1000)
                    if response.elapsed is not None
                    else None
                ),
            }
            
            logger.info("Successfully retrieved Astral API configuration")
            return result
            
    except httpx.TimeoutException:
        error_msg = f"Configuration request timed out after {DEFAULT_TIMEOUT} seconds"
        logger.error(error_msg)
        return {
            "success": False,
            "error": "timeout_error",
            "message": error_msg,
            "details": {"timeout_seconds": DEFAULT_TIMEOUT}
        }
        
    except httpx.HTTPStatusError as e:
        error_msg = f"Configuration request failed with status {e.response.status_code}"
        logger.error(f"{error_msg}: {e.response.text}")
        return {
            "success": False,
            "error": "api_error",
            "message": error_msg,
            "details": {
                "status_code": e.response.status_code,
                "response_text": e.response.text[:ERROR_TEXT_TRUNCATE_LENGTH],
            },
        }
        
    except Exception as e:
        error_msg = f"Unexpected error fetching configuration: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": "unexpected_error",
            "message": error_msg,
            "details": {"exception_type": type(e).__name__}
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
