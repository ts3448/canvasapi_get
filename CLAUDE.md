# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library for accessing the Canvas LMS API with unified async/sync operations. The library provides a synchronous interface while internally using async operations for optimal performance. 

**Important: This is a GET-only library** designed for read-only Canvas API access. It was derived from the full canvasapi library but modified to only support GET operations for safer, read-only interactions with Canvas data. For full CRUD operations, use the complete 'canvasapi' library instead.

Key architectural features:

- **Unified Request Architecture**: All API calls use `UnifiedRequester` which provides sync interface over async `AsyncRequester`
- **Background Event Loop**: `BackgroundLoop` singleton manages async operations from sync contexts
- **Concurrent Pagination**: `PaginatedList` automatically uses concurrent fetching for improved performance
- **Intelligent Rate Limiting**: `AsyncRateLimitState` and `RateLimitCoordinator` handle Canvas API rate limits
- **Compatibility Layer**: `SyncCompatibleResponse` ensures backward compatibility with requests.Response

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