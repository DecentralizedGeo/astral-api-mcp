## Phase 2 Session Prompts

### Session 2.1: `query_location_proofs` Tool Implementation

# FEATURE DEVELOPMENT SESSION

## Feature Overview

Implement `query_location_proofs`, the primary tool enabling users to query location attestations from the Astral API with comprehensive filtering capabilities.

## User Story Context

As an agent user, I want to search for location proofs (attestations) using chain, prover, and limit filters so I can analyze blockchain location activity and identify patterns in attestation data.

## Technical Scope

- **Modify/create:** `astral_mcp_server/server.py` (add new tool function)
- **Integrate with:** Astral REST API endpoint `GET /api/v0/location-proofs`
- **Data requirements:** Capture, decode, and structure JSON API responses with geospatial data
- **UI/UX requirements:** N/A (CLI/API interface)

## Implementation Strategy

1. **API Integration:** Implement REST call to `/api/v0/location-proofs` with proper async handling
2. **Parameter Support:** Add query parameters for chain, prover, limit, and offset with validation
3. **Response Processing:** Parse API results and structure for MCP host consumption
4. **Error Management:** Handle edge cases including bad inputs, no data found, and server errors
5. **Input Validation:** Comprehensive validation with user-friendly error messages

## Dependencies

- Requires completed MCP server skeleton from Phase 1
- Assumes Astral API is available at `https://api.astral.global/api/v0`
- Depends on `httpx` for HTTP client functionality

## Non-Functional Requirements

- **Performance:** Response within 2 seconds for standard limit sizes (≤50 results)
- **Security:** No sensitive data logged, proper input sanitization
- **Reliability:** Graceful degradation for network issues and API errors
- **Usability:** Clear, actionable error messages for invalid inputs

## Definition of Done

- [ ] Tool returns expected location proof lists with proper structure
- [ ] Handles all edge cases: invalid chains, malformed addresses, API timeouts
- [ ] Input validation covers all parameters with helpful error messages
- [ ] Tests validate input processing and API calling functionality
- [ ] Tool includes comprehensive docstring with parameter details and examples

## Open Questions

- Should the tool support pagination for large responses automatically?
- What's the preferred error message format for different MCP host applications?
- Should we implement client-side caching for frequently accessed queries?

**Are there any implementation preferences or specific filtering requirements before we proceed?**

### Session 2.2: `get_location_proof_by_uid` Tool Implementation

# FEATURE DEVELOPMENT SESSION

## Feature Overview

Enable retrieval of specific location proof attestations using their unique identifier, providing complete attestation details for detailed analysis.

## User Story Context

As a user, I want to fetch all details of a specific attestation using its unique identifier so I can examine the complete proof data, including raw attestation content, decoded fields, and verification evidence.

## Technical Scope

- **Modify/create:** Extend `astral_mcp_server/server.py` with new tool function
- **Integrate with:** Astral API `GET /api/v0/location-proofs/{uid}` endpoint
- **Data requirements:** Return complete record structure or structured not-found error
- **UI/UX requirements:** N/A (CLI/API interface)

## Implementation Strategy

1. **UID Parsing:** Validate UID format (66-character hex string starting with 0x)
2. **API Call:** Execute GET request to specific proof endpoint with proper error handling
3. **Response Processing:** Handle successful responses, 404 not found, and other HTTP errors
4. **Data Structure:** Return complete proof data including coordinates, timestamps, and verification info
5. **Error Context:** Provide meaningful errors that include the attempted UID for debugging

## Dependencies

- Astral API endpoint accessibility and proper response format
- Completed server skeleton with httpx client configuration
- Standard error handling patterns from the project

## Non-Functional Requirements

- **Security:** No exception traces leaked to end users, secure error handling
- **Performance:** Quick response for individual record retrieval (sub-1 second)
- **Reliability:** Robust handling of network timeouts and malformed UIDs
- **Usability:** Clear differentiation between not-found vs. system errors

## Definition of Done

- [ ] Tool accurately fetches and returns complete proof data for valid UIDs
- [ ] Handles not-found cases cleanly with informative error messages
- [ ] Processes malformed UIDs with helpful validation feedback
- [ ] Tests cover positive cases (valid UIDs) and negative cases (invalid/not-found)
- [ ] Error responses include the attempted UID for debugging context
- [ ] Tool docstring includes UID format requirements and example usage

## Open Questions

- Does the UID format ever change across different chains or remain consistent?
- Should we include both raw attestation data and decoded fields by default, or make this configurable?
- How should we handle UIDs that exist but point to non-location attestations?

**Any clarifications or additional requirements to discuss before implementation?**

### Session 2.3: `get_astral_config` Tool & Error Handling Standardization

# FEATURE DEVELOPMENT SESSION

## Feature Overview

Expose Astral API configuration information to users and standardize error handling patterns across all MCP server tools.

## User Story Context

As an AI agent or developer, I need to know which chains, schemas, and capabilities are supported by the Astral API so I can make informed queries and guide users toward valid parameter choices.

## Technical Scope

- **Modify/create:** Add `get_astral_config` tool to `astral_mcp_server/server.py`
- **Integrate with:** Astral REST API `/api/v0/config` endpoint
- **Data requirements:** Parse and format configuration response for consumption
- **Error handling:** Implement consistent error response format across all tools

## Implementation Strategy

1. **Config Endpoint:** REST call to `/api/v0/config` with timeout handling
2. **Response Formatting:** Structure config data for easy consumption by MCP hosts
3. **Error Standardization:** Apply consistent error response schema across all tools
4. **Logging Enhancement:** Add structured logging for debugging and monitoring
5. **Response Validation:** Ensure config data meets expected format requirements

## Dependencies

- Astral API configuration endpoint availability and stability
- Established HTTP client patterns from previous tool implementations
- Consistent error handling framework across the server

## Non-Functional Requirements

- **Security:** Configuration endpoint should never expose sensitive system information
- **Performance:** Config retrieval should be fast and could benefit from caching
- **Reliability:** Graceful failure when config endpoint is unavailable
- **Consistency:** All tools should use identical error response structure

## Definition of Done

- [ ] Returns comprehensive chain and schema information on successful requests
- [ ] Fails gracefully with informative errors when API is unavailable
- [ ] All existing tools use consistent error response format (success, error, details structure)
- [ ] Enhanced logging captures important events and errors for debugging
- [ ] Simple tests validate config output format and error handling
- [ ] Documentation includes config response structure and caching behavior

## Open Questions

- Should we expose API version information and sync status from the backend?
- Would local config caching improve performance, and if so, what's the appropriate TTL?
- Should the error standardization include response timing/performance metadata?

**Any further details to clarify about the configuration tool or error handling approach before coding?**
