## Phase 4 Session Prompts

### Session 4.1: Claude Desktop Integration

# INTEGRATION SESSION

## Integration Goal

Connect the Astral MCP server with Claude Desktop to enable real-world AI assistant usage with location attestation querying capabilities.

## Systems Overview

**System A (Astral MCP Server)**:

- Purpose: Query location proof attestations from Astral API via MCP protocol
- Key interfaces: MCP STDIO transport with 4 tools (health_check, query_location_proofs, get_location_proof_by_uid, get_astral_config)
- Data formats: JSON responses with location proofs, coordinates, and verification data
- Authentication: No authentication required (public read access)

**System B (Claude Desktop)**:

- Purpose: AI assistant interface that can utilize MCP servers for extended capabilities
- Key interfaces: MCP client protocol, JSON configuration file management
- Data formats: MCP protocol messages, tool call requests/responses
- Authentication: Local configuration file authorization

## Integration Requirements

- Data flow: Bidirectional MCP protocol communication via STDIO transport
- Error handling: Graceful error reporting from server to Claude with user-friendly messages
- Performance: Tool responses under 2 seconds for typical location queries
- Monitoring: Logging capability for debugging integration issues

## Technical Approach

1. **Configuration File Creation**: Generate proper `claude_desktop_config.json` with correct server path and environment settings
2. **Integration Testing**: Validate MCP server works correctly within Claude Desktop environment
3. **User Workflow Development**: Create example conversation flows and query patterns
4. **Troubleshooting Setup**: Establish debugging procedures for common integration issues

## Dependencies and Assumptions

- Completed and tested MCP server from Phase 3 with all tools functional
- Claude Desktop application installed and accessible on the development machine
- Poetry environment works correctly and can be invoked from Claude's process context
- Network connectivity allows access to Astral API endpoints from Claude's environment

## Testing Strategy

- Configuration validation: Verify Claude Desktop loads the MCP server without errors
- Tool functionality testing: Test all 4 tools work correctly within Claude conversations
- Error scenario testing: Validate error handling when API is unavailable or inputs are invalid
- Performance testing: Confirm response times meet sub-2 second requirement in real usage

## Rollback Plan

- Remove MCP server configuration from Claude Desktop config file
- Document configuration backup process for easy restoration
- Provide clear steps to disable integration if issues arise
- Establish monitoring indicators that suggest integration problems

## Open Questions

- Should we configure logging level differently for production Claude usage vs development?
- Do we need to handle any special cases for Claude Desktop's security or sandboxing?
- What level of usage examples should we provide for common location query patterns?

**What questions do you have about the Claude Desktop integration approach or any specific configuration requirements?**

### Session 4.2: VS Code Integration & Troubleshooting Guide

# INTEGRATION SESSION

## Integration Goal

Configure VS Code/Cursor integration as a secondary MCP host target and create comprehensive troubleshooting documentation for common integration issues.

## Systems Overview

**System A (Astral MCP Server)**:

- Purpose: Location attestation querying via MCP protocol
- Key interfaces: Same MCP STDIO tools as Claude Desktop integration
- Data formats: Consistent JSON responses across different MCP hosts
- Authentication: Public API access with no authentication required

**System B (VS Code/Cursor + MCP Extensions)**:

- Purpose: Code editor with AI assistant capabilities and MCP server support
- Key interfaces: MCP server configuration via extension settings, workspace configurations
- Data formats: MCP protocol messages, extension configuration JSON
- Authentication: Workspace-level configuration authorization

## Integration Requirements

- Data flow: MCP protocol communication via configured extensions
- Error handling: Extension-specific error reporting and debugging capabilities
- Performance: Consistent sub-2 second response times across different host environments
- Monitoring: Debug logging accessible through VS Code extension logs

## Technical Approach

1. **VS Code Configuration Setup**: Create extension-specific configuration for MCP server integration
2. **Cursor Integration**: Adapt configuration for Cursor-specific MCP support requirements
3. **Troubleshooting Guide Creation**: Develop comprehensive problem resolution documentation
4. **Cross-Platform Validation**: Ensure integration works on Windows, Mac, and Linux environments

## Dependencies and Assumptions

- VS Code with appropriate MCP extensions installed and functional
- Cursor application with MCP support capabilities available for testing
- Same Poetry environment and server setup from previous phases
- Documentation framework established for troubleshooting guide creation

## Testing Strategy

- Extension integration testing: Verify MCP server loads correctly in VS Code and Cursor
- Cross-platform validation: Test integration on multiple operating systems
- Error scenario documentation: Catalog common failure modes and solutions
- User experience testing: Validate setup process can be completed by new users

## Rollback Plan

- Document extension configuration removal process
- Provide clear steps to revert VS Code/Cursor settings
- Establish backup procedures for extension configurations
- Create monitoring checklist for integration health validation

## Open Questions

- Which VS Code MCP extensions are most reliable and well-maintained for our use case?
- Should the troubleshooting guide cover advanced debugging techniques or focus on common issues?
- Do we need separate configuration approaches for different VS Code MCP extensions?
- What level of cross-platform testing is realistic within the project timeline?

**Any specific concerns about VS Code integration complexity or particular troubleshooting scenarios you want to prioritize?**
