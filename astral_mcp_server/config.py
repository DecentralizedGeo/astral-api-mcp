"""
Configuration module for Astral MCP Server

Contains configuration constants and settings for the MCP server.
"""

import os
from typing import Optional

# Astral API Configuration
ASTRAL_API_BASE_URL = "https://api.astral.global"
ASTRAL_HEALTH_ENDPOINT = f"{ASTRAL_API_BASE_URL}/health"

# HTTP Client Configuration
DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 3

# MCP Server Configuration
SERVER_NAME = "astral-mcp-server"
SERVER_VERSION = "0.1.0"

def get_api_key() -> Optional[str]:
    """
    Retrieve API key from environment variables.
    
    Returns:
        Optional[str]: API key if set, None otherwise
    """
    return os.getenv("ASTRAL_API_KEY")