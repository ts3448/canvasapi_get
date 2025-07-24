# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library for accessing the Canvas LMS API with a hybrid architecture - it provides a synchronous public interface while being entirely async internally for optimal performance.

**Important: This is a GET-only library** designed for read-only Canvas API access. It was derived from the full canvasapi library but modified to only support GET operations for safer, read-only interactions with Canvas data. For full CRUD operations, use the complete 'canvasapi' library instead.

### Hybrid Architecture Design

**Public API: Synchronous**
- All methods you call are synchronous and return sync objects like `PaginatedList` and Canvas objects
- Maintains backward compatibility with the original canvasapi interface
- No async/await syntax exposed to end users

**Internal Implementation: Fully Async**
- Uses `AsyncRequester`, aiohttp, async pagination, and concurrent operations
- `BackgroundLoop` singleton runs async operations from sync contexts
- All HTTP operations go through async infrastructure for performance
- `UnifiedRequester.request()` only accepts GET methods for read-only safety

Key architectural features:

- **Unified Request Architecture**: `UnifiedRequester` provides sync interface over fully async `AsyncRequester`
- **Background Event Loop**: `BackgroundLoop` singleton manages async operations from sync contexts
- **Concurrent Pagination**: `PaginatedList` automatically uses concurrent fetching for improved performance
- **Intelligent Rate Limiting**: `AsyncRateLimitState` and `RateLimitCoordinator` handle Canvas API rate limits
- **Compatibility Layer**: `SyncCompatibleResponse` wraps async responses to maintain requests.Response compatibility
- **GET-Only Enforcement**: `UnifiedRequester` validates and restricts to GET operations only

## Async Pagination Implementation

### Core Pagination Strategy
This library implements an advanced pagination strategy that improves upon the original synchronous canvasapi:

1. **Parallel Page Fetching**: When a paginated endpoint is requested, the system:
   - Starts fetching the first page
   - Immediately begins fetching subsequent pages in parallel
   - Continues until an empty page is returned
   - Allows earlier pages to "catch up" for complete results

2. **Canvas API Pagination Format**: Canvas uses Link header pagination with rel="next" and rel="last" links
   - Pages are numbered starting from 1
   - Page size can be controlled via `per_page` parameter (max 100 for most endpoints)
   - Empty pages indicate end of data

3. **Rate Limit Aware Concurrency**: 
   - Respects Canvas API rate limits (typically 3000 requests/hour per token)
   - Uses async semaphores to control concurrent request count
   - Implements exponential backoff for rate limit responses

### Critical Implementation Details
- **Seek-Ahead Pattern**: System fetches pages beyond current position to detect pagination end early
- **Result Ordering**: Despite parallel fetching, results maintain correct page order
- **Error Isolation**: Individual page fetch failures don't break entire pagination sequence
- **Resource Cleanup**: Async context managers ensure proper HTTP client lifecycle management

## Canvas API Reference Integration

### Canvas REST API Documentation
Complete Canvas LMS REST API documentation is available in the `.claude/markdown_docs/` directory. These files contain detailed information about endpoints, parameters, and response formats:

@.claude/markdown_docs/

When working with this codebase, reference these comprehensive Canvas API documentation files for:
- **API Endpoints**: Complete endpoint documentation with parameters and examples
- **Authentication**: Bearer token authentication patterns and requirements  
- **Rate Limiting**: Canvas API rate limit specifications and best practices
- **Pagination**: Link header pagination patterns and implementation details
- **Error Responses**: Standard HTTP status codes and Canvas-specific error formats
- **Canvas Objects**: Objects are abstract and dynamic, and should use the existing dynamic attribute generation
- **Include Parameters**: Available include options for embedding related data

## Core Architecture

### Request Flow
1. **Canvas Class**: Main entry point (`canvasapi_get/canvas.py`)
2. **UnifiedRequester**: Bridges sync/async (`canvasapi_get/unified_requester.py`)
3. **AsyncRequester**: Handles HTTP with rate limiting (`canvasapi_get/async_requester.py`)
4. **BackgroundLoop**: Manages async execution (`canvasapi_get/background_loop.py`)

### Async Infrastructure Components
- **AsyncRequester**: Core HTTP client using aiohttp with rate limiting
- **BackgroundLoop**: Event loop management for sync-over-async pattern
- **AsyncRateLimitState**: Tracks API usage and enforces limits
- **RateLimitCoordinator**: Coordinates rate limiting across multiple requesters
- **PaginatedList**: Async-aware pagination with concurrent fetching

### Key Components
- **Canvas Objects**: Each Canvas entity (Course, User, etc.) inherits from `CanvasObject`
- **Pagination**: `PaginatedList` provides automatic concurrent page fetching
- **Rate Limiting**: Shared state across all requesters via `RateLimitCoordinator`
- **Error Handling**: Custom exceptions in `exceptions.py` for different HTTP error codes

### Module Structure
- Core API objects are in individual files (e.g., `course.py`, `user.py`, `assignment.py`)
- Utility modules: `util.py`, `canvas_object.py`, `exceptions.py`
- Async infrastructure: `async_*.py`, `background_loop.py`, `unified_requester.py`
- Rate limiting: `rate_limit_*.py` files

## MCP Server Expansion Plan

### Overview
The library is being expanded with MCP (Model Context Protocol) server functionality to enable intelligent Canvas data analysis and troubleshooting. This expansion maintains backward compatibility while adding powerful new capabilities for data filtering, analysis, and automated problem diagnosis.

### MCP Architecture Strategy

**Three-Tool Design**: The MCP server provides three complementary tools that work together to enable comprehensive Canvas API access:

1. **discover_canvas_methods** - Dynamically explores available Canvas API methods by object type
2. **get_canvas_method_info** - Provides detailed information about specific methods including parameters and documentation  
3. **canvas_query** - Executes Canvas API calls with DataFrame/CSV output options

This approach supports all 300+ Canvas methods automatically through dynamic discovery and resolution, eliminating the need for hardcoded method mappings while providing intelligent exploration capabilities.

### Key MCP Features

**1. Dynamic Method Discovery**
- **discover_canvas_methods**: Explore available Canvas API methods by object type with filtering
- **get_canvas_method_info**: Get detailed method documentation, parameters, and signatures
- Dynamic resolution discovers and validates available methods without hardcoded mappings
- Preserves existing async performance and rate limiting

**2. Universal Canvas Query Execution**
- **canvas_query**: Execute any Canvas API method with parameter validation
- Supports both direct Canvas methods and object-specific method calls
- GET-only operations for safe, read-only Canvas interactions
- Comprehensive error handling with actionable error messages

**3. Universal DataFrame Conversion**
- Converts any Canvas object/response to pandas DataFrame
- Handles PaginatedList, single objects, and raw API responses
- Maintains consistent column naming and data type conversion
- Memory-efficient processing for large datasets (1000+ records)
- Multiple output formats: table, JSON, CSV, summary statistics

**4. Environment-Based Security**
- Secure configuration through environment variables (CANVAS_URL, CANVAS_TOKEN)
- No hardcoded credentials in configuration files
- Health check validation for Canvas connectivity
- Comprehensive logging for debugging and monitoring

### MCP Module Structure

The MCP functionality is implemented as a sibling directory to maintain clean separation:

```
canvasapi_get/
├── canvasapi_get/             # Core library (unchanged)
│   ├── __init__.py
│   ├── canvas.py
│   └── ...
├── canvasapi_mcp/             # MCP server (new sibling)
│   ├── __init__.py
│   ├── server.py              # Main MCP server with environment-based config
│   ├── tools/
│   │   ├── canvas_query.py    # Universal Canvas query execution
│   │   └── method_discovery.py # Dynamic method discovery tools
│   ├── resolvers/
│   │   └── method_resolver.py # Dynamic method resolution
│   ├── utils/
│   │   ├── dataframe_converter.py # Canvas object → DataFrame
│   │   └── attribute_discovery.py # Semantic attribute search
│   └── validation.py          # Parameter validation
├── examples/                  # Configuration examples
│   ├── README.md              # Setup and configuration guide
│   ├── claude_desktop_config.json # Example client configuration
│   └── mcp_client_config.json # Generic MCP client config
└── pyproject.toml             # Updated with optional [mcp] extra
```

### MCP Development Phases

**Phase 1: Core Infrastructure** ✅ **COMPLETE**
- ✅ Dynamic method resolution system (`resolvers/method_resolver.py`)
- ✅ Canvas object → MCP tool parameter mapping (`validation.py`)
- ✅ Basic MCP server setup with error handling (`server.py`)
- ✅ Universal Canvas query tool (`tools/canvas_query.py`)
- ✅ MCP dependencies configuration with optional `[mcp]` extra

**Phase 2: DataFrame Conversion** ✅ **COMPLETE**
- ✅ Universal Canvas object to DataFrame converter (`utils/dataframe_converter.py`)
- ✅ Attribute flattening and data type normalization for nested Canvas objects
- ✅ Large dataset optimization and streaming for PaginatedList processing
- ✅ Column naming standardization and data type inference
- ✅ Memory-efficient batch processing for 1000+ record datasets
- ✅ Support for all Canvas object types with consistent schema mapping
- ✅ Semantic attribute discovery system (`utils/attribute_discovery.py`)
- ✅ Extended canvas_query tool with DataFrame/CSV output formats

**Phase 2.5: Dynamic Discovery** ✅ **COMPLETE**
- ✅ Dynamic Canvas method discovery (`tools/method_discovery.py`)
- ✅ **discover_canvas_methods** tool for exploring available Canvas API methods
- ✅ **get_canvas_method_info** tool for detailed method documentation
- ✅ Eliminated hardcoded Canvas method mappings in favor of dynamic resolution
- ✅ Environment-based configuration for secure Canvas URL/token management
- ✅ Comprehensive client configuration examples (`examples/` directory)
- ✅ Health check validation for Canvas connectivity testing

#### Phase 2 Implementation Details

**Core Components:**
1. **DataFrameConverter Class** (`utils/dataframe_converter.py`)
   - Convert any Canvas object or PaginatedList to pandas DataFrame
   - Handle nested object flattening with configurable depth limits
   - Implement streaming conversion for large datasets
   - Support batch processing with memory management

2. **Schema Mapping System**
   - Consistent column naming across all Canvas object types
   - Data type inference and conversion (dates, IDs, booleans)
   - Handle Canvas-specific data formats (ISO dates, SIS IDs)
   - Maintain backward compatibility with existing Canvas object attributes

3. **Memory Optimization**
   - Streaming processor for PaginatedList with configurable batch sizes
   - Memory-efficient iterator patterns for large datasets
   - Lazy loading with on-demand DataFrame construction
   - Garbage collection optimization for batch processing

4. **Attribute Discovery Enhancement** (`utils/attribute_discovery.py`)
   - Semantic attribute search across Canvas objects
   - Relationship mapping between different Canvas object types
   - Dynamic schema discovery for unknown Canvas object types
   - Metadata extraction for DataFrame column information

**Integration Points:**
- Extend `canvas_query` tool with DataFrame output format option
- Integrate with existing `validation.py` for parameter handling
- Use `PaginatedList` async iteration for streaming conversion
- Leverage `CanvasObject` dynamic attributes for schema discovery

**Performance Requirements:**
- Handle 1000+ record datasets efficiently
- Batch processing with configurable memory limits
- Concurrent conversion for multiple Canvas object types
- Sub-second conversion for typical Canvas query results

**Output Formats:**
- Standard pandas DataFrame with optimized dtypes
- JSON-serializable DataFrame representations for MCP responses  
- CSV export capability for large datasets
- Summary statistics and metadata for DataFrame inspection

**Phase 3: Pandas Operations Engine**
- Safe pandas query execution with allowlisted methods
- Sequential operation processing pipeline
- Advanced filtering and aggregation capabilities

**Phase 4: MCP Server Integration**
- Complete MCP tool implementation
- Server configuration and deployment setup
- Concurrent request handling

**Phase 5: Troubleshooting Intelligence**
- Email-based user diagnostic tools
- Pattern recognition for common Canvas issues
- Cross-reference analysis across multiple data sources

### MCP Benefits

**Enhanced Canvas Data Access**
- Single unified interface for all Canvas operations
- Advanced SQL-like filtering on Canvas data
- Leverages existing concurrent pagination performance
- Automatic support for new Canvas methods via dynamic discovery

**Intelligent Troubleshooting**
- Email-based user lookup and issue diagnosis
- Cross-reference analysis combining multiple Canvas data sources
- Pattern recognition for common Canvas problems
- Structured diagnostic reports with actionable recommendations

**Client Experience**
- No bulk data transfer - clients receive only filtered results
- Pandas power without client-side complexity
- Multiple output formats (table, JSON, CSV, summary)
- Consistent interface pattern for all Canvas operations

### MCP Technical Requirements

**New Dependencies**
```toml
[tool.poetry.dependencies]
pandas = "^2.0.0"          # DataFrame operations
mcp = "^1.0.0"             # MCP protocol implementation
numpy = "^1.24.0"          # pandas dependency
```

**Integration Points**
- Uses existing `UnifiedRequester` for sync-over-async operations
- Preserves `PaginatedList` concurrent fetching benefits
- Maintains all rate limiting and performance optimizations
- No modifications required to core Canvas API code

## Development Guidelines

### Async/Sync Pattern Requirements
- **All API methods must remain synchronous** for backward compatibility
- Internal implementation should use `UnifiedRequester` which handles async execution
- Never expose async/await in public API surface
- Use `BackgroundLoop` to run async operations from sync contexts

### Adding New Canvas Objects
1. Create new module in `canvasapi_get/` following existing patterns
2. Inherit from `CanvasObject` base class
3. Import and expose in `canvas.py` main class
4. Add to `__init__.py` exports if needed
5. Methods should be alphabetically ordered (checked by `scripts/alphabetic.py`)

### Request Methods
- All API calls should use `self._requester.request()` (inherited from CanvasObject)
- Use `**kwargs` for optional parameters (checked by `scripts/find_missing_kwargs.py`)
- Return `PaginatedList` for paginated endpoints, single objects otherwise
- **Never use requests library directly** - all HTTP should go through async infrastructure

### Pagination Implementation
- Use `PaginatedList` for all paginated Canvas API endpoints
- Let the async pagination system handle concurrency automatically
- Don't implement manual pagination loops - rely on the unified system
- Test pagination with both small and large datasets

### Rate Limiting Compliance
- All requests automatically respect Canvas API rate limits
- Don't implement custom rate limiting - use the shared `RateLimitCoordinator`
- Handle rate limit exceptions gracefully with exponential backoff
- Consider rate limit impact when designing bulk operations

### MCP Development Guidelines

**MCP Module Development**
- Keep MCP functionality in `canvasapi_mcp/` sibling directory
- Use dynamic method resolution instead of hardcoded Canvas method lists
- Preserve all async performance benefits in MCP operations
- Implement proper error handling and validation for MCP tools

**DataFrame Conversion Standards**
- Convert all Canvas objects to consistent DataFrame format
- Handle nested attributes through flattening strategies
- Maintain data type consistency across different Canvas objects
- Optimize memory usage for large dataset conversions

**Pandas Operations Safety**
- Use allowlisted pandas methods only in operations engine  
- Validate all user-provided pandas operation parameters
- Implement safe execution context for DataFrame operations
- Provide clear error messages for unsafe or invalid operations

### Code Quality
- Code style enforced by black, isort, and flake8
- Functions must be alphabetically ordered within classes
- Google-style docstrings required for all public methods
- Use type hints with modern Python syntax (no `typing` imports needed)
- **Async code must use proper context management** for resource cleanup

## Troubleshooting Common Issues

### Async/Sync Integration Problems
- **Event loop conflicts**: Use `BackgroundLoop` singleton, never create additional loops
- **Blocking async calls**: Ensure all async operations go through `UnifiedRequester`
- **Resource leaks**: Always use async context managers for HTTP clients

### Pagination Issues  
- **Missing results**: Verify parallel page fetching doesn't skip pages
- **Out-of-order results**: Ensure `PaginatedList` maintains page order despite concurrent fetching
- **Rate limit errors**: Check that concurrent pagination respects API limits

### Canvas API Integration
- **Authentication failures**: Verify API token has required scopes
- **Unexpected pagination**: Some Canvas endpoints have non-standard pagination behavior
- **SIS ID conflicts**: Handle both Canvas IDs and SIS IDs consistently

### MCP-Specific Troubleshooting

**Server Configuration Issues**
- **"Canvas URL is required"**: Set `CANVAS_URL` or `CANVAS_BASE_URL` environment variable
- **"Canvas API token is required"**: Set `CANVAS_TOKEN`, `CANVAS_API_TOKEN`, or `CANVAS_API_KEY` environment variable
- **"Failed to resolve"**: Verify Canvas URL is correct and accessible from server environment
- **"Authentication failed"**: Check API token validity and Canvas instance permissions

**Method Discovery Issues**
- **"No method found for object type"**: Use `discover_canvas_methods` to explore available methods
- **"Method not found on object"**: Verify method exists using `get_canvas_method_info` tool
- **"Method is not a GET operation"**: This library only supports GET operations for safety

**Query Execution Problems**
- **Parameter validation errors**: Check required parameters using `get_canvas_method_info`
- **Canvas API errors**: Verify Canvas API limits, permissions, and object IDs
- **DataFrame conversion failures**: Use smaller batch sizes for large datasets

**Client Configuration**
- **MCP server not found**: Verify Python path and canvasapi_mcp module installation
- **Environment variables not loaded**: Check MCP client configuration includes `env` section
- **Connection timeouts**: Increase timeout settings or check network connectivity