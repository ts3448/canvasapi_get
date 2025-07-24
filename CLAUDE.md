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

**Generic Tool Design**: Instead of creating individual MCP tools for each Canvas method, the expansion implements a single universal `canvas_query` tool with method chaining:

```python
canvas_query(
    method="get_courses",           # Canvas method name
    from_object="account",          # Source object for method chaining
    from_object_id=439,            # ID of source object
    parameters={                    # Canvas API method parameters
        "enrollment_term_id": 583
    },
    pandas_operations=[             # Flexible DataFrame operations
        {
            "operation": "query",
            "params": {"expr": "name.str.contains('CHEM')"}
        },
        {
            "operation": "sort_values", 
            "params": {"by": "enrollment_count", "ascending": False}
        }
    ],
    output_format="table"           # Response format
)
```

### Key MCP Features

**1. Method Chaining Resolution**
- Natural Canvas API flow: `canvas.get_account(439)` → `account.get_courses()` → DataFrame operations
- Dynamic method resolution supports all 300+ Canvas methods automatically
- Preserves existing async performance and rate limiting

**2. Universal DataFrame Conversion**
- Converts any Canvas object/response to pandas DataFrame
- Handles PaginatedList, single objects, and raw API responses
- Maintains consistent column naming and data type conversion
- Memory-efficient processing for large datasets (1000+ records)

**3. Flexible Pandas Operations Engine**
- Safe execution with allowlisted pandas methods
- Sequential operation processing: query → sort → filter → aggregate
- SQL-like operations on Canvas data without client-side complexity
- Error handling for unsafe operations

**4. Intelligent Troubleshooting**
- Email-based user lookup and diagnostic data gathering
- Cross-reference multiple Canvas data sources (enrollments, courses, assignments)
- Pattern recognition for common Canvas issues
- Actionable diagnostic reports

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
│   ├── server.py              # Main MCP server
│   ├── tools/
│   │   └── canvas_query.py    # Generic query tool
│   ├── resolvers/
│   │   └── method_resolver.py # Method chaining resolver
│   ├── utils/
│   │   ├── dataframe_converter.py # Canvas object → DataFrame
│   │   ├── pandas_engine.py   # Safe pandas operations
│   │   └── attribute_discovery.py # Semantic attribute search
│   └── validation.py          # Parameter validation
└── pyproject.toml             # Updated with optional [mcp] extra
```

### MCP Development Phases

**Phase 1: Core Infrastructure**
- Method chaining resolution system
- Canvas object → MCP tool parameter mapping
- Basic MCP server setup with error handling

**Phase 2: DataFrame Conversion**
- Universal Canvas object to DataFrame converter
- Attribute flattening and data type normalization
- Large dataset optimization and streaming

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

**Method Resolution Issues**
- **Unknown methods**: Verify Canvas method exists using dynamic discovery
- **Parameter validation**: Check Canvas API documentation for required/optional parameters
- **Object chaining**: Ensure `from_object` and `from_object_id` resolve to valid Canvas objects

**DataFrame Conversion Problems**
- **Memory issues**: Use streaming conversion for large PaginatedLists
- **Data type conflicts**: Verify attribute flattening handles nested Canvas objects
- **Missing columns**: Check that DataFrame converter handles all Canvas object attributes

**Pandas Operations Failures**
- **Unsafe operations**: Verify pandas method is in allowlisted operations
- **Invalid expressions**: Validate query expressions against DataFrame columns  
- **Operation sequencing**: Ensure pandas operations are applied in correct order