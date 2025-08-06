# Astral API MCP Server Agent

We are exploring the development of a Model Context Protocol (MCP) agent that integrates with the Astral API to enable intelligent querying and analysis of attestations submitted to the Ethereum Attestation Service (EAS). This agent would support complex queries across spatial and temporal dimensions, such as filtering attestations by schema ID, location, or date range, while maintaining persistent context across sessions. By leveraging Astral’s structured API and EAS’s open schema model, the agent could automate common analytical workflows—like generating attestation heatmaps or tracking schema usage over time—making it a valuable tool for both research and production use cases. This early scoping phase would help assess feasibility and determine if this direction merits further investment.

Table of Contents

- [Astral API MCP Server Agent](#astral-api-mcp-server-agent)
  - [The Benefits of an Astral API MCP Server Agent](#the-benefits-of-an-astral-api-mcp-server-agent)
    - [✅ Structured, Repetitive Queries](#-structured-repetitive-queries)
    - [✅ Well-Defined Interface](#-well-defined-interface)
    - [✅ Long-Term Guidance](#-long-term-guidance)
    - [✅ Domain-Specific Memory](#-domain-specific-memory)
    - [✅ Multi-Tool Orchestration](#-multi-tool-orchestration)
    - [Examples of What the Agent Could Do](#examples-of-what-the-agent-could-do)
- [Building a Simple MCP Server for Querying Location Attestations](#building-a-simple-mcp-server-for-querying-location-attestations)
  - [Project Overview](#project-overview)
  - [Technical Foundation](#technical-foundation)
    - [EAS Data Access](#eas-data-access)
    - [MCP Server Architecture](#mcp-server-architecture)
  - [Stage 1 Implementation Plan](#stage-1-implementation-plan)
  - [Phase 1: Environment Setup and Server Foundation](#phase-1-environment-setup-and-server-foundation)
  - [Phase 2: Core Tools Implementation with Integrated Error Handling](#phase-2-core-tools-implementation-with-integrated-error-handling)
    - [Tool 1: `query_location_proofs`](#tool-1-query_location_proofs)
    - [Tool 2: `get_location_proof_by_uid`](#tool-2-get_location_proof_by_uid)
    - [Tool 3: `get_astral_config`](#tool-3-get_astral_config)
  - [Phase 3: MCP Inspector Testing and Debugging](#phase-3-mcp-inspector-testing-and-debugging)
  - [Phase 4: Real-World Integration Setup](#phase-4-real-world-integration-setup)
  - [Phase 5: Documentation and Production Readiness](#phase-5-documentation-and-production-readiness)
  - [Core Tools Specification](#core-tools-specification)
    - [1. Query Location Proofs Tool](#1-query-location-proofs-tool)
    - [2. Get Location Proof by UID Tool](#2-get-location-proof-by-uid-tool)
    - [3. Get API Configuration Tool](#3-get-api-configuration-tool)
  - [Supported Networks](#supported-networks)
  - [Success Criteria](#success-criteria)
  - [Effort Estimation](#effort-estimation)
  - [Technology Stack](#technology-stack)

## The Benefits of an Astral API MCP Server Agent

The criteria and signals suggesting the potential value of developing an MCP agent include:

- **Performing Repetitive or Structured Tasks:** If your workflow involves sequences like "edit > test > deploy" or "extract > transform > validate > load", you can encode this in an MCP agent.
- **A Well-Defined Interface**: MCP agents benefit from clear APIs, command-line tools, or schema definitions.
- **User Benefits from Domain-Specific Memory**: If the domain has specialized knowledge or conventions, an MCP agent trained or configured for it is very effective.

Considering these criteria, the **Astral API** is an strong candidate for the development for an MCP agent, delivering impactful results by enabling users to interact with the blockchain using natural language.

### ✅ Structured, Repetitive Queries

Querying for attestations using filters like:

- `schemaId`
- `recipient`
- `time range`
- `location (geohash, bounding box, etc.)`

These are structured, and could be templated or refined interactively.

> ⚙️ **MCP value**: Build reusable query patterns and tune them over time. Agent could even **optimize or explain** GraphQL queries.

---

### ✅ Well-Defined Interface

The [Astral API](https://docs.astral.global/api-reference) is RESTful and documented. EAS itself has a GraphQL API with known endpoints.

> 🔗 **MCP value**: Agents can call these APIs directly (e.g. using `requests` or `gql`), or generate sample queries to test in tools like Postman or Insomnia.

---

### ✅ Long-Term Guidance

You might want to:

- Explore changes in attestation volume over time or space.
- Compare similar schemas.
- Track schema adoption or agent behavior.

> 📈 **MCP value**: The agent can "remember" earlier query patterns, datasets, or discoveries — helping you **build insights iteratively**.

---

### ✅ Domain-Specific Memory

EAS + Astral is niche: schemas are typed, attestations may include geospatial, identity, or sensor data. There’s a **need for domain grounding**.

> 🌐 **MCP value**: The agent can store knowledge about:

- Schema IDs → their structure and intent
- Key coordinate systems or standards
- Mapping schema fields to human concepts

---

### ✅ Multi-Tool Orchestration

In practice, a typical work flow might look like this:

1. Query Astral API endpoint for attestations
2. Join results with off chain metadata or external datasets
3. Visualize or analyze results (e.g. with Folium, Deck.gl, or Leaflet)
4. Store or re-attest

> 🤖 **MCP value**: You can build an assistant that coordinates all of this — it could:

- Generate Python scripts for each part
- Keep track of the bounding box you’re exploring
- Suggest next steps based on results

---

### Examples of What the Agent Could Do

With memory + tooling, an MCP agent could:

- "Show all attestations for schema `0xabc...` in California between May and June."
- "Has anyone attested to this location in the last 90 days?"
- "Generate a heatmap of attestation density in the last week."
- "Summarize attestations for `solar-panel-reading` schema over time."

---

# Building a Simple MCP Server for Querying Location Attestations

The following outlines a simplified scope for building a basic Model Context Protocol (MCP) server that can query attestations from the Ethereum Attestation Service (EAS). By focusing on core functionality, this project is designed to be achievable within a short development duration.

## Project Overview

**Goal:** Create a basic MCP (Model Context Protocol) server that enables AI models to query attestations from the Ethereum Attestation Service (EAS) using the available Astral GraphQL endpoints and APIs.

## Technical Foundation

### EAS Data Access

The Astral API provides a unified REST interface to query location proof attestations from multiple blockchains:[^1][^2][^3]

- **Astral API:** Primary endpoint at `https://api.astral.global/api/v0/location-proofs` with comprehensive location attestation access
- **Geospatial Indexing:** Built-in spatial query capabilities and geographic filtering
- **Multi-Chain Support:** Automatic synchronization with Arbitrum, Base, Celo, and Sepolia
- **No Authentication Required:** Public read access for location proof queries (currently)
- **Real-time Sync:** Background synchronization runs every minute to keep data fresh

### MCP Server Architecture

Based on the research, we'll use **Python with FastMCP** for rapid development:[^5][^6]

- **Framework:** `mcp` Python package with FastMCP class[^6][^7]
- **Package Manager:** `poetry` for dependency management and virtual environments
- **Transport:** STDIO for local development and testing[^5][^6]
- **Tools:** 3 core tools for querying attestations
- **Development Time:** 1 week for basic functionality

## Stage 1 Implementation Plan

The following outlines the initial implementation plan (which we will refer to as "Stage 1") for the MCP server, broken down into 5 phases:

## Phase 1: Environment Setup and Server Foundation

**Duration:** 1-2 days

**Combined Goals:** Set up the development environment and create a working MCP server skeleton with proper foundation.

**Deliverables:**

- Python project structure with Poetry dependency management
- MCP server skeleton using FastMCP with proper metadata and documentation
- Astral API connectivity verification tool
- Basic project configuration files (`.gitignore`, `README.md`)
- Initial Claude Desktop configuration template

**MCP Best Practices Integration:**

```python
from mcp.server.fastmcp import FastMCP
import httpx
from typing import Optional

# Proper server initialization with metadata
mcp = FastMCP(
    name="astral-location-server",
    version="0.1.0",
    description="MCP server for querying location attestations via Astral API"
)

@mcp.tool()
async def health_check() -> dict:
    """Verify connectivity to Astral API endpoints
    
    Returns:
        dict: API health status and configuration info
    """
    # Implementation with proper error handling
```

## Phase 2: Core Tools Implementation with Integrated Error Handling

**Duration:** 2-3 days

**Unified Goal:** Implement all three core tools with robust error handling, input validation, and proper MCP conventions built-in from the start.

**Core Tools with Enhanced Specifications:**

### Tool 1: `query_location_proofs`

```python
@mcp.tool()
async def query_location_proofs(
    chain: Optional[str] = None,
    prover: Optional[str] = None, 
    limit: int = 10,
    offset: int = 0
) -> dict:
    """Query location proofs from Astral API with comprehensive filtering
    
    Args:
        chain: Blockchain network (arbitrum, base, celo, sepolia)
        prover: Ethereum address of the attestation creator  
        limit: Maximum results (1-100, default 10)
        offset: Pagination offset (default 0)
    
    Returns:
        dict: Location proofs with metadata, coordinates, and verification data
        
    Raises:
        ValueError: For invalid parameters
        TimeoutError: For API timeout
    """
```

### Tool 2: `get_location_proof_by_uid`

```python
@mcp.tool()
async def get_location_proof_by_uid(uid: str) -> dict:
    """Retrieve specific location proof by unique identifier
    
    Args:
        uid: Location proof unique identifier (64-character hex string)
        
    Returns:
        dict: Complete location proof details including raw and decoded data
    """
```

### Tool 3: `get_astral_config`

```python
@mcp.tool() 
async def get_astral_config() -> dict:
    """Get Astral API configuration and supported capabilities
    
    Returns:
        dict: Supported chains, schemas, API version, and sync status
    """
```

**Integrated Error Handling Pattern:**

- Input validation before API calls
- Comprehensive HTTP error handling with meaningful messages
- Rate limiting awareness and timeout handling
- Structured error responses for MCP hosts

## Phase 3: MCP Inspector Testing and Debugging

**Duration:** 1 day

**Goal:** Thorough testing using MCP development tools and resolving any protocol-level issues.

**Deliverables:**

- Complete MCP Inspector test suite covering all tools
- Test scenarios for edge cases and error conditions  
- Performance validation (sub-2 second response times)
- Debug logging configuration for development

**Testing Commands:**

```bash
# MCP Inspector testing
poetry run mcp dev server.py

# Validate all tools work correctly
poetry run python -m pytest tests/
```

## Phase 4: Real-World Integration Setup

**Duration:** 1-2 days

**Goal:** Configure and test integration with actual MCP host applications.

**Target Integrations:**

1. **Claude Desktop** (Primary) - Complete configuration and testing
2. **VS Code with Cursor/Claude extensions** (Secondary) - Basic configuration

**Deliverables:**

- Tested Claude Desktop configuration file
- VS Code MCP server configuration
- Integration troubleshooting guide
- Example queries and workflows for each platform

**Claude Desktop Configuration:**

```json
{
  "mcpServers": {
    "astral-location-server": {
      "command": "poetry",
      "args": ["run", "python", "server.py"],
      "cwd": "/path/to/astral-mcp-server",
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## Phase 5: Documentation and Production Readiness

**Duration:** 1 day

**Goal:** Create comprehensive documentation and prepare for broader usage.

**Deliverables:**

- Complete README with installation, configuration, and usage
- API documentation for all tools with examples
- Troubleshooting guide for common integration issues
- Example query patterns and use cases
- Basic deployment considerations (logging, monitoring, configuration management)

**Documentation Structure:**

```
docs/
├── ai/
├── Quick Start
├── Installation & Setup  
├── Integration Guides
│   ├── Claude Desktop
│   └── VS Code/Cursor
├── API Reference
├── Example Queries
└── Troubleshooting
```

## Core Tools Specification

### 1. Query Location Proofs Tool

- **Purpose:** Search location proof attestations with filters
- **Parameters:** chain, prover, limit, offset (optional)
- **Output:** List of location proofs with decoded geospatial data

### 2. Get Location Proof by UID Tool

- **Purpose:** Retrieve specific location proof details
- **Parameters:** uid
- **Output:** Full location proof details including coordinates, media, and verification data

### 3. Get API Configuration Tool

- **Purpose:** Get Astral API configuration and capabilities
- **Parameters:** None
- **Output:** Supported chains, schema information, and API version details

## Supported Networks

Focus on Astral API supported blockchains:[^1][^2][^3]

- **Arbitrum:** Supported by Astral API
- **Base:** Supported by Astral API  
- **Celo:** Supported by Astral API
- **Sepolia (Ethereum testnet):** Supported by Astral API for development and testing

The Astral API automatically synchronizes with these networks, providing fresh data without requiring direct blockchain connections.

## Success Criteria

1. **Functional MCP Server:** Successfully connects and responds to MCP protocol messages
2. **Working Tools:** All 3 tools execute successfully and return valid data
3. **AI Integration:** Works with at least one MCP host (Claude Desktop recommended)
4. **Error Handling:** Gracefully handles network failures and invalid inputs and provides useful feedback to users.
5. **Documentation:** Clear setup and usage instructions

**Success Metrics:**

- [ ] All tools work reliably in Claude Desktop or VS Code as secondary integration target.
- [ ] Response times under 2 seconds for typical queries
- [ ] Error handling provides useful feedback to users
- [ ] Documentation enables easy setup by new users
- [ ] Integration works out-of-the-box with provided configurations

## Effort Estimation

- **Total Duration:** ~1 week (7-9 days)
- **Complexity:** Beginner to Intermediate
- **Prerequisites:** Basic Python knowledge, familiarity with GraphQL concepts

## Technology Stack

- **Language:** Python 3.12+
- **Framework:** FastMCP from `mcp` package[^5][^6]
- **HTTP Client:** `httpx` for GraphQL requests[^7]
- **Package Manager:** `poetry` for modern Python development and dependency management
- **Testing:** MCP Inspector for development testing[^7]

This simplified scope focuses on core functionality and practical learning, giving you hands-on experience with MCP server development while working with real blockchain data from EAS. The 1-week timeline is achievable for someone with basic Python knowledge and provides a solid foundation for extending to the more comprehensive Astral API integration later.

<div style="text-align: center">⁂</div>

[^1]: <https://github.com/ethereum-attestation-service/eas-contracts>

[^2]: <https://docs.verifiedpools.com/developers/verifications>

[^3]: <https://www.quicknode.com/guides/ethereum-development/smart-contracts/what-is-ethereum-attestation-service-and-how-to-use-it>


[^5]: <https://github.com/modelcontextprotocol/python-sdk>

[^6]: <https://composio.dev/blog/mcp-server-step-by-step-guide-to-building-from-scrtch>

[^7]: <https://modelcontextprotocol.io/quickstart/server>


