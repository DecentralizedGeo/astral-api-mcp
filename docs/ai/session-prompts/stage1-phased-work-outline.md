
# MCP Astral Server - Phase-by-Phase Work Outlines

## Phase 1: Environment Setup and Server Foundation

**Duration:** 1-2 days | **Sessions:** 2 focused sessions

### Session 1.1: Python Environment \& Project Structure Setup

**Context Window Focus:** Project initialization and dependency management

**Session Objectives:**

- Set up Poetry-managed Python project
- Configure development environment
- Establish project structure following Python best practices

**Specific Tasks:**

```bash
# Project initialization commands to include in session
poetry new astral-mcp-server
cd astral-mcp-server
poetry add "mcp[cli]" httpx
poetry add --group dev pytest black flake8 mypy
```

**File Structure to Create:**

```text
astral-mcp-server/
├── astral_mcp_server/
│   ├── __init__.py
│   ├── server.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   └── test_server.py
├── pyproject.toml
├── README.md
└── .gitignore
```

**Session Deliverables:**

- Working Poetry environment
- Project structure with proper imports
- Basic `pyproject.toml` configuration
- Initial `.gitignore` and `README.md`

**Success Criteria:**

- `poetry install` runs without errors
- `poetry run python -c "import astral_mcp_server"` works
- Project structure follows Python package conventions

---

### Session 1.2: MCP Server Skeleton \& Astral API Connectivity

**Context Window Focus:** MCP server foundation and API integration

**Session Objectives:**

- Implement basic MCP server using FastMCP
- Create health check tool for Astral API
- Establish proper error handling patterns

**Core Implementation:**

```python
# astral_mcp_server/server.py
from mcp.server.fastmcp import FastMCP
import httpx
import asyncio
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server with proper metadata
mcp = FastMCP(
    name="astral-location-server",
    version="0.1.0", 
    description="MCP server for querying location attestations via Astral API"
)

ASTRAL_BASE_URL = "https://api.astral.global/api/v0"

@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """Verify connectivity to Astral API endpoints
    
    Returns:
        dict: API health status and configuration info
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{ASTRAL_BASE_URL}/health")
            if response.status_code == 200:
                return {
                    "status": "healthy",
                    "api_accessible": True,
                    "response_time_ms": response.elapsed.total_seconds() * 1000,
                    "api_version": response.headers.get("x-api-version", "unknown")
                }
            else:
                return {
                    "status": "unhealthy",
                    "api_accessible": False,
                    "error": f"HTTP {response.status_code}"
                }
    except httpx.TimeoutException:
        return {"status": "timeout", "api_accessible": False, "error": "Request timeout"}
    except Exception as e:
        return {"status": "error", "api_accessible": False, "error": str(e)}

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**Session Deliverables:**

- Working MCP server skeleton
- Functional health check tool
- Basic Claude Desktop configuration template
- Error handling foundation

**Success Criteria:**

- Server starts without errors: `poetry run python astral_mcp_server/server.py`
- Health check returns valid response
- MCP Inspector can connect: `poetry run mcp dev astral_mcp_server/server.py`

---

## Phase 2: Core Tools Implementation with Integrated Error Handling

**Duration:** 2-3 days | **Sessions:** 3 focused sessions

### Session 2.1: `query_location_proofs` Tool Implementation

**Context Window Focus:** Primary query functionality with comprehensive filtering

**Session Objectives:**

- Implement main location proof querying tool
- Add input validation and error handling
- Support pagination and filtering parameters

**Tool Implementation:**

```python
@mcp.tool()
async def query_location_proofs(
    chain: Optional[str] = None,
    prover: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> Dict[str, Any]:
    """Query location proofs from Astral API with comprehensive filtering
    
    Args:
        chain: Blockchain network (arbitrum, base, celo, sepolia)
        prover: Ethereum address of the attestation creator
        limit: Maximum results (1-100, default 10)
        offset: Pagination offset (default 0)
    
    Returns:
        dict: Location proofs with metadata, coordinates, and verification data
    """
    
    # Input validation
    if limit < 1 or limit > 100:
        return {"error": "limit must be between 1 and 100", "success": False}
    
    if offset < 0:
        return {"error": "offset must be non-negative", "success": False}
    
    valid_chains = ["arbitrum", "base", "celo", "sepolia"]
    if chain and chain.lower() not in valid_chains:
        return {"error": f"chain must be one of {valid_chains}", "success": False}
    
    if prover and not prover.startswith("0x"):
        return {"error": "prover must be a valid Ethereum address starting with 0x", "success": False}
    
    # Build query parameters
    params = {"limit": limit, "offset": offset}
    if chain:
        params["chain"] = chain.lower()
    if prover:
        params["prover"] = prover
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{ASTRAL_BASE_URL}/location-proofs", params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "results": data.get("results", []),
                    "total": data.get("total", 0),
                    "limit": limit,
                    "offset": offset,
                    "query_params": params
                }
            else:
                return {
                    "error": f"API returned status {response.status_code}",
                    "success": False,
                    "details": response.text[:200] if response.text else None
                }
                
    except httpx.TimeoutException:
        return {"error": "Request timed out", "success": False}
    except Exception as e:
        logger.error(f"Error in query_location_proofs: {e}")
        return {"error": f"Unexpected error: {str(e)}", "success": False}
```

**Session Deliverables:**

- Complete `query_location_proofs` tool
- Comprehensive input validation
- Structured error responses
- Unit tests for the tool

**Success Criteria:**

- Tool handles various input combinations correctly
- Error messages are informative and actionable
- API responses are properly parsed and formatted

---

### Session 2.2: `get_location_proof_by_uid` Tool Implementation

**Context Window Focus:** Individual record retrieval with full details

**Session Objectives:**

- Implement UID-based proof retrieval
- Handle not-found scenarios gracefully
- Return complete proof details including raw and decoded data

**Tool Implementation:**

```python
@mcp.tool()
async def get_location_proof_by_uid(uid: str) -> Dict[str, Any]:
    """Retrieve specific location proof by unique identifier
    
    Args:
        uid: Location proof unique identifier (64-character hex string)
        
    Returns:
        dict: Complete location proof details including raw and decoded data
    """
    
    # Input validation
    if not uid:
        return {"error": "uid parameter is required", "success": False}
    
    if not uid.startswith("0x") or len(uid) != 66:  # 0x + 64 hex chars
        return {"error": "uid must be a 66-character hex string starting with 0x", "success": False}
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{ASTRAL_BASE_URL}/location-proofs/{uid}")
            
            if response.status_code == 200:
                proof_data = response.json()
                return {
                    "success": True,
                    "proof": proof_data,
                    "uid": uid
                }
            elif response.status_code == 404:
                return {
                    "error": f"Location proof with UID {uid} not found",
                    "success": False,
                    "uid": uid
                }
            else:
                return {
                    "error": f"API returned status {response.status_code}",
                    "success": False,
                    "uid": uid,
                    "details": response.text[:200] if response.text else None
                }
                
    except httpx.TimeoutException:
        return {"error": "Request timed out", "success": False, "uid": uid}
    except Exception as e:
        logger.error(f"Error in get_location_proof_by_uid: {e}")
        return {"error": f"Unexpected error: {str(e)}", "success": False, "uid": uid}
```

---

### Session 2.3: `get_astral_config` Tool \& Error Handling Standardization

**Context Window Focus:** Configuration retrieval and system-wide error handling patterns

**Session Objectives:**

- Implement configuration information tool
- Standardize error handling across all tools
- Add logging and monitoring infrastructure

**Tool Implementation:**

```python
@mcp.tool()
async def get_astral_config() -> Dict[str, Any]:
    """Get Astral API configuration and supported capabilities
    
    Returns:
        dict: Supported chains, schemas, API version, and sync status
    """
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{ASTRAL_BASE_URL}/config")
            
            if response.status_code == 200:
                config_data = response.json()
                return {
                    "success": True,
                    "config": config_data,
                    "retrieved_at": datetime.now().isoformat()
                }
            else:
                return {
                    "error": f"Failed to retrieve config: HTTP {response.status_code}",
                    "success": False,
                    "details": response.text[:200] if response.text else None
                }
                
    except httpx.TimeoutException:
        return {"error": "Request timed out while fetching config", "success": False}
    except Exception as e:
        logger.error(f"Error in get_astral_config: {e}")
        return {"error": f"Unexpected error: {str(e)}", "success": False}
```

**Session Deliverables:**

- Complete `get_astral_config` tool
- Standardized error response format across all tools
- Enhanced logging infrastructure
- Comprehensive test suite for all tools

---

## Phase 3: MCP Inspector Testing and Debugging

**Duration:** 1 day | **Sessions:** 1 intensive session

### Session 3.1: Comprehensive Testing \& Debug Resolution

**Context Window Focus:** Testing all tools and resolving integration issues

**Session Objectives:**

- Test all tools using MCP Inspector
- Validate error handling scenarios
- Ensure protocol compliance
- Document any issues and resolutions

**Testing Commands:**

```bash
# Start MCP Inspector
poetry run mcp dev astral_mcp_server/server.py

# Test scenarios to validate:
# 1. health_check tool - should return API status
# 2. query_location_proofs - test various parameter combinations
# 3. get_location_proof_by_uid - test valid/invalid UIDs  
# 4. get_astral_config - should return configuration
```

**Test Scenarios Matrix:**

```python
# Test cases to implement
test_scenarios = [
    # Health check tests
    {"tool": "health_check", "params": {}, "expected": "success"},
    
    # Query tests - valid inputs
    {"tool": "query_location_proofs", "params": {"limit": 5}, "expected": "success"},
    {"tool": "query_location_proofs", "params": {"chain": "base", "limit": 10}, "expected": "success"},
    
    # Query tests - invalid inputs
    {"tool": "query_location_proofs", "params": {"limit": 150}, "expected": "error"},
    {"tool": "query_location_proofs", "params": {"chain": "invalid"}, "expected": "error"},
    
    # UID tests
    {"tool": "get_location_proof_by_uid", "params": {"uid": "0x" + "a" * 64}, "expected": "not_found_ok"},
    {"tool": "get_location_proof_by_uid", "params": {"uid": "invalid"}, "expected": "error"},
    
    # Config test
    {"tool": "get_astral_config", "params": {}, "expected": "success"}
]
```

**Session Deliverables:**

- All tools working correctly in MCP Inspector
- Performance validation (sub-2 second responses)
- Debug logging properly configured
- Issue resolution documentation

---

## Phase 4: Real-World Integration Setup

**Duration:** 1-2 days | **Sessions:** 2 focused sessions

### Session 4.1: Claude Desktop Integration

**Context Window Focus:** Claude Desktop configuration and testing

**Session Objectives:**

- Configure Claude Desktop integration
- Create working configuration files
- Test real-world usage scenarios
- Document integration process

**Claude Desktop Configuration:**

```json
{
  "mcpServers": {
    "astral-location-server": {
      "command": "poetry",
      "args": ["run", "python", "astral_mcp_server/server.py"],
      "cwd": "/absolute/path/to/astral-mcp-server",
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**Testing Prompts for Claude:**

```text
# Test prompts to validate integration:
1. "Check if the Astral API is healthy"
2. "Query for 5 location proofs on the Base network"
3. "Get the Astral API configuration"
4. "Search for location proofs from a specific prover address"
```

---

### Session 4.2: VS Code Integration \& Troubleshooting Guide

**Context Window Focus:** Secondary integration target and problem resolution

**Session Objectives:**

- Set up VS Code/Cursor integration
- Create troubleshooting documentation
- Test common error scenarios
- Document resolution steps

**VS Code Configuration Example:**

```json
{
  "mcp.servers": {
    "astral-location-server": {
      "command": ["poetry", "run", "python", "astral_mcp_server/server.py"],
      "cwd": "/path/to/astral-mcp-server"
    }
  }
}
```

**Troubleshooting Guide Template:**

```markdown
# Common Issues and Solutions

## Issue: "Server failed to start"
- Check Poetry environment: `poetry install`
- Verify Python version: `python --version` (should be 3.10+)
- Check logs in MCP host application

## Issue: "API timeout errors"
- Verify internet connection
- Check Astral API status at https://api.astral.global/api/v0/health
- Increase timeout in server.py if needed

## Issue: "Invalid parameters"
- Review tool documentation for correct parameter formats
- Check that chain names are lowercase
- Ensure UIDs start with '0x' and are 66 characters long
```

---

## Phase 5: Documentation and Production Readiness

**Duration:** 1 day | **Sessions:** 1 comprehensive session

### Session 5.1: Documentation \& Production Polish

**Context Window Focus:** Complete documentation and deployment preparation

**Session Objectives:**

- Create comprehensive README and documentation
- Add example usage patterns
- Prepare for broader distribution
- Add basic production considerations

**Documentation Structure:**

```markdown
# Astral MCP Server

## Quick Start
[Installation and basic usage]

## Installation & Setup
[Detailed setup instructions]

## Integration Guides
### Claude Desktop
[Step-by-step Claude integration]

### VS Code/Cursor  
[IDE integration instructions]

## API Reference
[Complete tool documentation with examples]

## Example Queries
[Common usage patterns and workflows]

## Troubleshooting
[Problem resolution guide]
```

**Example Usage Patterns:**

```python
# Example queries to document:

# 1. Basic location search
query_location_proofs(chain="base", limit=10)

# 2. Targeted prover search  
query_location_proofs(prover="0x742d35Cc6635C0532925a3b8D26c3C6632f78B9", limit=5)

# 3. Retrieve specific proof
get_location_proof_by_uid("0xa1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456")

# 4. Check system capabilities
get_astral_config()
```

**Session Deliverables:**

- Complete README.md with all sections
- API reference documentation
- Integration examples for multiple platforms
- Troubleshooting guide
- Basic logging and monitoring setup

**Success Criteria:**

- Documentation enables new user setup in <15 minutes
- All integration examples work out-of-the-box
- Common issues have documented solutions
- Server is ready for broader distribution

---

## Session Management Tips

**For Each Session:**

1. **Start with clear context** - Review previous session outcomes
2. **Focus on single objectives** - Don't try to accomplish multiple phases in one session
3. **Test incrementally** - Validate each component before moving forward
4. **Document as you go** - Keep notes on decisions and issues encountered
5. **End with clear handoff** - Document what's complete and what's next

**Context Window Management:**

- Keep each session focused on 1-2 related tools/features
- Include relevant code snippets and examples in the session
- Reference external documentation via URLs rather than copying large blocks
- Use structured formats (JSON, YAML) for configuration examples

This breakdown ensures each session is manageable within typical LLM context windows while building systematically toward a complete, production-ready MCP server.[^1][^2][^3]

<div style="text-align: center">⁂</div>

[^1]: https://huggingface.co/blog/tsadoq/agent2agent-and-mcp-tutorial

[^2]: https://os.platformstud.io/guild/articles/llm-context-window-size-the-new-moore-s-law-by-jeremy-burton

[^3]: https://codingscape.com/blog/llms-with-largest-context-windows

[^4]: agent-session-templates.md

[^5]: project-overview.md

[^6]: https://modelcontextprotocol.io/docs/learn/architecture

[^7]: https://simplescraper.io/blog/how-to-mcp

[^8]: https://github.com/lastmile-ai/mcp-agent

[^9]: https://www.jeeva.ai/blog/multi-agent-coordination-playbook-(mcp-ai-teamwork)-implementation-plan

[^10]: https://www.anthropic.com/research/building-effective-agents

[^11]: https://composio.dev/blog/mcp-client-step-by-step-guide-to-building-from-scratch

[^12]: https://ssojet.com/blog/what-are-the-best-practices-for-mcp-security

[^13]: https://www.linkedin.com/pulse/ultimate-guide-model-context-protocol-mcp-pavan-belagatti-kqm3c

[^14]: http://rlancemartin.github.io/2025/06/23/context_engineering/

[^15]: https://www.youtube.com/watch?v=IjbTvHs-Sa4

[^16]: https://www.getzep.com/ai-agents/developer-guide-to-mcp

[^17]: https://www.reddit.com/r/LocalLLaMA/comments/1eplndh/what_is_the_current_largest_context_window_for_an/

[^18]: https://www.getambassador.io/blog/mcp-server-explained

[^19]: https://devblogs.microsoft.com/blog/can-you-build-agent2agent-communication-on-mcp-yes

[^20]: https://www.letta.com/blog/memory-blocks

[^21]: https://www.getambassador.io/blog/model-context-protocol-mcp-connecting-llms-to-apis

[^22]: https://community.openai.com/t/hypothesis-stabilizing-llm-agent-behavior-via-archetypal-anchoring-user-side-framework/1249964
