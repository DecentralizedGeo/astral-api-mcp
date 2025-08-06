## Phase 1 Session Prompts

### Session 1.1: Python Environment & Project Structure Setup

# PROJECT FOUNDATION SESSION

## High-Level Goal

Establish a reproducible Python development environment with Poetry dependency management and proper project structure for the Astral MCP server.

## Current Context

- Project type: CLI/MCP server backend tool
- Technology stack: Python 3.12+, Poetry, FastMCP framework
- Development stage: Greenfield project initialization
- Team size: Solo developer

## Session Scope

Create foundational project structure, configure Poetry environment, and establish development workflow basics.

## Specific Deliverables

1. **Poetry-managed Python project** - Complete `pyproject.toml` with proper metadata and dependencies
2. **Project directory structure** - Organized package layout following Python conventions
3. **Development configuration** - `.gitignore`, basic `README.md`, and development setup
4. **Environment validation** - Confirmed working virtual environment and dependency installation

## Constraints

- Use Poetry exclusively (not pip or conda) for dependency management
- Follow PEP 517/518 standards for project configuration
- Maintain cross-platform compatibility (Windows, Mac, Linux)
- Structure must support future MCP server development

## Success Criteria

- [ ] `poetry install` successfully creates virtual environment and installs dependencies
- [ ] Project structure follows Python package conventions with proper `__init__.py` files
- [ ] `poetry run python -c "import astral_mcp_server"` executes without errors
- [ ] All configuration files are properly formatted and documented

## Open Questions

- Should we include development dependencies (pytest, black, mypy) in the initial setup?
- Do you prefer a flat or nested package structure for the server components?

**What questions do you have before we initialize the project structure?**

### Session 1.2: MCP Server Skeleton & Astral API Connectivity

# PROJECT FOUNDATION SESSION

## High-Level Goal

Bootstrap the MCP server using FastMCP framework and establish reliable connectivity to the Astral API with proper error handling.

## Current Context

- Project type: Python MCP server with REST API integration
- Technology stack: FastMCP (`mcp[cli]`), httpx for HTTP requests
- Development stage: Post-environment setup, server foundation
- Dependencies: Completed Poetry environment from Session 1.1

## Session Scope

Install core MCP dependencies, implement basic server skeleton with proper metadata, and create health check functionality for Astral API connectivity.

## Specific Deliverables

1. **MCP dependency installation** - Add `mcp[cli]` and `httpx` via Poetry with proper version constraints
2. **FastMCP server skeleton** - Basic `server.py` with proper initialization, metadata, and async support
3. **Astral API health check tool** - Functional tool that verifies API connectivity and returns status
4. **Development validation setup** - Confirm server launches and responds to MCP Inspector connections

## Constraints

- Use asynchronous programming patterns (`async def`) throughout
- Follow MCP protocol standards for tool definitions and responses
- Implement comprehensive error handling for network requests
- Include proper logging infrastructure for debugging

## Success Criteria

- [ ] Server starts successfully with `poetry run python astral_mcp_server/server.py`
- [ ] MCP Inspector can connect: `poetry run mcp dev astral_mcp_server/server.py`
- [ ] Health check tool returns valid response from `https://api.astral.global/api/v0/health`
- [ ] All tools include proper docstrings with parameter and return type documentation
- [ ] Error handling gracefully manages network timeouts and API failures

## Open Questions

- Should we implement configuration file support for API endpoints at this stage?
- What level of detail do you want in the health check response (basic status vs. detailed metrics)?

**Do you need any clarifications about the MCP server architecture before implementation?**
---
