# MCP Tools Guide for Astral API

This guide provides comprehensive documentation for the MCP (Model Context Protocol) tools available in the Astral API MCP server, along with example prompts and usage patterns.

## Configuration

### API Endpoint Selection

The MCP server supports both production and development Astral API endpoints. You can configure which endpoint to use:

**Via Environment Variable** (highest priority):

```bash
export ASTRAL_USE_DEV_ENDPOINT=true
```

**Via MCP Configuration** (`.vscode/mcp.json`):

```json
{
  "servers": {
    "astral-api": {
      "command": "poetry",
      "args": ["run", "start-server"],
      "cwd": "${workspaceFolder}",
      "type": "stdio"
    }
  },
  "mcp_agent": {
    "use_dev_endpoint": true,
    "dev_endpoint": "https://custom-dev-api.example.com"
  }
}
```

**Configuration Options**:

- `use_dev_endpoint`: Set to `true` to use the development API endpoint
- `dev_endpoint` (optional): Override the default dev endpoint URL with a custom one

The server will log which endpoint is being used on startup. This is useful for:

- Testing against development versions of the API
- Using custom or staging endpoints
- Switching between environments without code changes

## Available MCP Tools

The Astral MCP server provides 5 main tools for interacting with the Astral API:

1. [**health_check**](#1-health-check-check_astral_api_health) - Check API connectivity
2. [**server_info**](#2-server-info-get_server_info) - Get server metadata and capabilities
3. [**query_location_proofs**](#3-query-location-proofs-query_location_proofs) - Search location attestations with filters
4. [**get_location_proof_by_uid**](#4-get-location-proof-by-uid-get_location_proof_by_uid) - Fetch specific attestation by UID
5. [**get_astral_config**](#5-get-astral-config-get_astral_config) - Get API configuration and supported chains

---

## Tool Documentation & Examples

### 1. Health Check (`check_astral_api_health`)

**Purpose**: Verify connectivity and availability of the Astral API service.

**Parameters**: None

**Example Prompts**:

```text
Check if the Astral API is healthy and responding #check_astral_api_health
#check_astral_api_health Is the Astral service up and running?
Verify API connectivity #check_astral_api_health
```

**Use Cases**:

- Troubleshooting connectivity issues
- Service monitoring and status checks
- Initial validation before making data requests

---

### 2. Server Info (`get_server_info`)

**Purpose**: Retrieve metadata about the MCP server including capabilities and configuration status.

**Parameters**: None

**Example Prompts**:

```text
#get_server_info Show me information about this MCP server
#get_server_info What capabilities does this server have?
```

**Use Cases**:

- Understanding available server capabilities
- Verifying configuration status
- Getting server version and metadata

---

### 3. Query Location Proofs (`query_location_proofs`)

**Purpose**: Search and filter location attestations from the Astral network.

**Parameters**:

- `chain` (optional): Filter by blockchain network (e.g., "ethereum", "polygon")
- `prover` (optional): Filter by prover wallet address
- `subject` (optional): Filter by subject wallet address
- `from_timestamp` (optional): ISO date string to filter proofs after this timestamp
- `to_timestamp` (optional): ISO date string to filter proofs before this timestamp
- `bbox` (optional): Bounding box coordinates as `[minLng,minLat,maxLng,maxLat]` (comma-separated string or array)
- `limit` (optional): Maximum results to return (default: 10, max: 100)
- `offset` (optional): Results to skip for pagination (default: 0)
- `geojson_block` (optional): Include GeoJSON FeatureCollection output (aliases: `geojson=true`, `featureCollection=true`)

**Example Prompts**:

```text
Show me the latest 10 location proofs #query_location_proofs
Find location attestations on the ethereum chain #query_location_proofs
Get location proofs from prover address 0x1234... #query_location_proofs
Show 20 location proofs with pagination offset 10 #query_location_proofs and include the featureCollection output
Find attestations for subject 0xabcd... from the last week #query_location_proofs
Get location proofs within bounding box -122.5,37.7,-122.3,37.8 #query_location_proofs
Query proofs from January 1st to February 1st, 2025 #query_location_proofs
```

**Advanced Usage**:

```text
#query_location_proofs Find location attestations on polygon network with limit 25
#query_location_proofs Get the next 10 results after offset 20 for ethereum chain
#query_location_proofs Show location proofs from wallet 0xabcd... geojson=true
#query_location_proofs Filter by subject 0x1234... and prover 0x5678... on ethereum
#query_location_proofs Get proofs from timestamp 2025-01-01T00:00:00Z to 2025-01-31T23:59:59Z
#query_location_proofs Find attestations in San Francisco bbox -122.5,37.7,-122.3,37.8 with limit 50
```

**Use Cases**:

- Exploring recent location attestations
- Analyzing activity by specific provers or subjects
- Chain-specific location data analysis
- Time-based analysis and historical queries
- Geographic filtering within specific regions
- Pagination through large datasets
- Geographic visualization preparation

---

### 4. Get Location Proof by UID (`get_location_proof_by_uid`)

**Purpose**: Retrieve complete details for a specific location attestation using its unique identifier.

**Parameters**:

- `uid` (required): 66-character hex string starting with 0x
- `geojson_block` (optional): Include GeoJSON FeatureCollection output (aliases: `geojson=true`, `featureCollection=true`)

**Example Prompts**:

```text
Get details for location proof UID 0x1234567890abcdef... #get_location_proof_by_uid
Show me the complete attestation for UID 0xabcd... #get_location_proof_by_uid and include the geojson output
Fetch location proof 0x9876... #get_location_proof_by_uid
```

**Use Cases**:

- Deep-dive analysis of specific attestations
- Verification of attestation details
- Media content and proof examination
- Geographic coordinate extraction

---

### 5. Get Astral Config (`get_astral_config`)

**Purpose**: Retrieve configuration information including supported chains, schemas, and API capabilities.

**Parameters**: None

**Example Prompts**:

```text
#get_astral_config What chains does the Astral API support?
#get_astral_config Show me the available configuration options
#get_astral_config Get the current API schema and capabilities
```

**Use Cases**:

- Understanding supported blockchain networks
- Schema validation and planning
- API capability discovery
- Integration planning

---

## Working with Results

### Standard Response Format

All tools return structured JSON responses with consistent formatting:

```json
{
  "success": true,
  "data": { /* tool-specific data */ },
  "response_code": 200,
  "response_time_ms": 150
}
```

### Error Handling

Failed requests include error details:

```json
{
  "success": false,
  "error": "validation_error",
  "message": "Invalid parameter: uid format incorrect",
  "details": { /* additional error context */ }
}
```

### GeoJSON Output

When `geojson_block=true` is used, tools return two JSON blocks:

1. Standard result data
2. GeoJSON FeatureCollection for mapping

> You can tailor the prompting experience so the agent can recognize and apply aliases to parameters for a more natural interaction. Check out the [Assistant Style Guidelines](docs/ai/assistant-style.md) for more details.

---

## Pagination Strategies

For large datasets, use pagination effectively:

```text
# Start with recent data
Query the latest 10 location proofs

# Continue pagination
Get the next 10 location proofs with offset 10

# Large batch processing
Show 50 location proofs starting from offset 100
```

---

## Advanced Query Patterns

### Chain-Specific Analysis

```text
Show location proofs on ethereum chain with limit 20
Find polygon network attestations from the last batch
```

### Prover Investigation

```text
Get all recent location proofs from wallet 0x742d35Cc6634C0532925a3b8D...
Show attestation history for prover 0xabcd... with pagination
```

### Subject Analysis

```text
Find all attestations for subject 0x1234... across all chains
Get location proofs where subject 0xabcd... was attested by prover 0x5678...
```

### Temporal Filtering

```text
Query location proofs from the last 24 hours
Get attestations between 2025-01-01 and 2025-01-31
Find proofs submitted after 2025-02-15T10:00:00Z
```

### Geographic Filtering

```text
Get location proofs within San Francisco bay area (bbox: -122.5,37.7,-122.3,37.8)
Find attestations in a specific geographic region with custom bounding box
Query proofs within coordinates and include GeoJSON for mapping
```

### Geographic Data Extraction

```text
Query location proofs with GeoJSON for mapping
Get location proof 0x1234... with geographic coordinates
```

---

## Assistant Style Configuration

### Using Assistant Style Guidelines

This MCP server includes comprehensive assistant style guidelines (see `docs/ai/assistant-style.md`) that define:

- **Response Structure**: Consistent Summary → Key Details → Next Actions format
- **Formatting Conventions**: Table layouts, inline code formatting, and link generation
- **Geographic Integration**: Automatic map links (OpenStreetMap, Google Maps, Bing Maps)
- **Media Handling**: IPFS gateway links for attestation media content
- **Error Presentation**: Structured error reporting with actionable next steps

### Applying Style Rules

When using MCP Inspector or other AI assistants:

1. **Paste Style Instructions**: Copy the content from `assistant-style.md` into your AI assistant's system prompt
2. **Enable Consistent Formatting**: Responses will follow the defined structure automatically
3. **Get Enhanced Output**: Receive formatted tables, map links, and structured navigation suggestions

### Benefits of Style Guidelines

- **Consistency**: All responses follow the same clear structure
- **Actionability**: Every response includes suggested next steps
- **Visual Appeal**: Data presented in readable tables and formatted lists
- **Geographic Context**: Automatic map links for location data
- **Navigation Support**: Built-in pagination and exploration suggestions

### Example Styled Response

With style guidelines applied, a query response becomes:

**Summary**: Retrieved 5 location attestations from ethereum chain successfully.

**Key Details**:

| Location Attestation UID | Chain | Prover Address | Timestamp | Map Links |
|--------------------------|-------|----------------|-----------|-----------|
| 0x1234... | ethereum | 0xabcd... | 2025-08-15T10:30:00Z | [OpenStreetMap](https://...) [Google Maps](https://...) |

**Next Actions**:

- View detailed attestation for UID 0x1234...
- Query more proofs from prover 0xabcd...
- Get next page with offset 5

---

## Best Practices

1. **Start Small**: Begin with default limits (10 results) for exploration
2. **Use Filters**: Apply chain and prover filters to narrow focus
3. **Enable GeoJSON**: Include geographic data when location analysis is needed
4. **Paginate Thoughtfully**: Use appropriate batch sizes for your use case
5. **Verify UIDs**: Ensure UID format is correct (66-char hex starting with 0x)
6. **Apply Style Guidelines**: Use the assistant style rules for consistent, actionable responses

---

## Integration Examples

### Data Analysis Workflow

```text
1. Check if the Astral API is healthy
2. Get server info to verify capabilities
3. Query recent location proofs for overview
4. Filter by specific chain or prover for focused analysis
5. Fetch detailed attestations by UID for deep investigation
```

### Geographic Visualization Workflow

```text
1. Query location proofs with geojson_block=true
2. Extract coordinate data for mapping
3. Use generated map links for quick geographic reference
4. Fetch specific attestations for detailed location context
```

### Monitoring and Alerting Workflow

```text
1. Regular health checks for service availability
2. Query recent attestations for activity monitoring
3. Track specific prover addresses for compliance
4. Alert on unusual patterns or service disruptions
```
