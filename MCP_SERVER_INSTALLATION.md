# Canvas API MCP Server - Installation & Usage Guide

## Overview

The Canvas API MCP Server provides intelligent access to Canvas LMS data through the Model Context Protocol (MCP). It features server-side data filtering, dynamic method discovery, and seamless integration with Canvas APIs.

## Key Features

- **4 Powerful MCP Tools**:
  - `discover_canvas_methods` - Explore available Canvas API methods
  - `get_canvas_method_info` - Get detailed method documentation  
  - `get_pandas_operations` - Server-side data filtering operations
  - `canvas_query` - Execute Canvas API calls with filtering

- **Server-Side Processing**: Full Canvas datasets retrieved via async pagination, then filtered server-side
- **Memory Efficient**: Clients receive only filtered results, not bulk data  
- **Safe Operations**: Allowlisted pandas methods prevent unsafe code execution
- **Dynamic Discovery**: No hardcoded Canvas method mappings

## Installation

### Prerequisites

- Python 3.10 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Canvas LMS API token with appropriate permissions

### Quick Installation

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   source $HOME/.local/bin/env
   ```

2. **Install the Canvas API MCP Server**:
   ```bash
   # Install from the project directory
   cd /path/to/canvasapi_get
   uv sync --extra mcp
   
   # Or install from a repository
   uv add "canvasapi-get[mcp] @ git+https://github.com/your-repo/canvasapi_get.git"
   ```

3. **Test the installation**:
   ```bash
   uv run canvasapi-mcp --version
   # Should output: Canvas API MCP Server 0.1.0
   ```

## Configuration

### Getting Your Canvas API Token

1. Log into your Canvas instance
2. Go to **Account** → **Settings**
3. Scroll to **Approved Integrations**
4. Click **New Access Token**
5. Enter a purpose (e.g., "MCP Server Access")
6. Click **Generate Token**
7. **Copy and save the token immediately** (you won't see it again)

### Environment Variables

The server supports these environment variables:

#### Canvas Configuration (Required)
- `CANVAS_URL` or `CANVAS_BASE_URL` - Your Canvas instance URL
- `CANVAS_TOKEN`, `CANVAS_API_TOKEN`, or `CANVAS_API_KEY` - Your Canvas API token

#### Optional Settings
- `MCP_SERVER_NAME` - Server instance name (default: "canvas-api")

### Example Environment Setup

Create a `.env` file in your project directory:
```bash
CANVAS_URL=https://your-school.instructure.com
CANVAS_TOKEN=1234~your-api-token-here
MCP_SERVER_NAME=canvas-api
```

## MCP Client Configuration

### For Claude Desktop

1. **Find your Claude Desktop config file**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`

2. **Add the Canvas MCP server configuration**:
   ```json
   {
     "mcpServers": {
       "canvas-api": {
         "command": "uv",
         "args": [
           "--directory",
           "/absolute/path/to/canvasapi_get",
           "run",
           "canvasapi-mcp"
         ],
         "env": {
           "CANVAS_URL": "https://your-school.instructure.com",
           "CANVAS_TOKEN": "your-api-token-here"
         }
       }
     }
   }
   ```

3. **Replace the values**:
   - Update `/absolute/path/to/canvasapi_get` with your actual project path
   - Replace `https://your-school.instructure.com` with your Canvas URL
   - Replace `your-api-token-here` with your actual API token

4. **Restart Claude Desktop**

### Alternative: Using Direct Command

You can also run the server directly:
```json
{
  "mcpServers": {
    "canvas-api": {
      "command": "canvasapi-mcp",
      "env": {
        "CANVAS_URL": "https://your-school.instructure.com", 
        "CANVAS_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

### For Other MCP Clients

Use the appropriate configuration format for your MCP client, ensuring:
- The command runs the Canvas MCP server  
- Environment variables `CANVAS_URL` and `CANVAS_TOKEN` are set
- The server is accessible in the client's environment

## Testing Your Setup

### 1. Test Server Startup

```bash
# Set environment variables
export CANVAS_URL="https://your-school.instructure.com"
export CANVAS_TOKEN="your-api-token-here"

# Run the server (will start and wait for MCP client connections)
uv run canvasapi-mcp
```

The server will perform a health check and report any configuration issues.

### 2. Test with Debug Logging

```bash
uv run canvasapi-mcp --log-level DEBUG
```

### 3. Verify Configuration

```bash
# Test that your Canvas credentials work
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://your-school.instructure.com/api/v1/users/self"
```

If this works, your credentials are correct.

## Available MCP Tools

Once configured, the MCP server provides these tools:

### 1. `discover_canvas_methods`
Explore available Canvas API methods by object type.

**Example Usage**:
```json
{
  "tool": "discover_canvas_methods",
  "arguments": {
    "object_type": "canvas"
  }
}
```

### 2. `get_canvas_method_info`  
Get detailed information about specific Canvas methods.

**Example Usage**:
```json
{
  "tool": "get_canvas_method_info",
  "arguments": {
    "object_type": "canvas",
    "method_name": "get_course"
  }
}
```

### 3. `get_pandas_operations`
Get information about server-side data filtering operations.

**Example Usage**:
```json
{
  "tool": "get_pandas_operations",
  "arguments": {
    "list_all": true,
    "include_examples": true
  }
}
```

### 4. `canvas_query`
Execute Canvas API calls with optional server-side filtering.

**Basic Example**:
```json
{
  "tool": "canvas_query", 
  "arguments": {
    "object_type": "canvas",
    "method": "get_courses",
    "output_format": "dataframe"
  }
}
```

**Advanced Example with Filtering**:
```json
{
  "tool": "canvas_query",
  "arguments": {
    "object_type": "course",
    "object_id": 12345,
    "method": "get_enrollments",
    "pandas_operations": [
      {"operation": "query", "expr": "enrollment_state == 'active'"},
      {"operation": "sort_values", "by": "created_at", "ascending": false},
      {"operation": "head", "n": 50}
    ],
    "output_format": "csv"
  }
}
```

## Common Use Cases

### 1. Explore Available Methods
```json
{"tool": "discover_canvas_methods", "arguments": {"object_type": "canvas"}}
```

### 2. Get Course Information
```json
{
  "tool": "canvas_query",
  "arguments": {
    "object_type": "canvas", 
    "method": "get_course",
    "parameters": {"course_id": 12345, "include": ["students", "assignments"]}
  }
}
```

### 3. Get Filtered Student Data
```json
{
  "tool": "canvas_query",
  "arguments": {
    "object_type": "course",
    "object_id": 12345,
    "method": "get_users",
    "pandas_operations": [
      {"operation": "query", "expr": "enrollment_state == 'active'"},
      {"operation": "sort_values", "by": "sortable_name"}
    ],
    "output_format": "dataframe"
  }
}
```

### 4. Generate Course Statistics
```json
{
  "tool": "canvas_query",
  "arguments": {
    "object_type": "course",
    "object_id": 12345,
    "method": "get_enrollments",
    "pandas_operations": [
      {"operation": "groupby", "by": "enrollment_state", "as_index": false},
      {"operation": "agg", "func": {"count": "count"}}
    ],
    "output_format": "json"
  }
}
```

## Troubleshooting

### Common Issues & Solutions

#### 1. "Canvas URL is required"
**Problem**: Missing Canvas URL configuration  
**Solution**: Set `CANVAS_URL` environment variable or pass `--canvas-url`

#### 2. "Canvas API token is required"
**Problem**: Missing API token  
**Solution**: Set `CANVAS_TOKEN` environment variable or pass `--canvas-token`

#### 3. "Failed to resolve"
**Problem**: Canvas URL is incorrect or inaccessible  
**Solution**: Verify Canvas URL is correct and accessible from server

#### 4. "Authentication failed"
**Problem**: Invalid or expired API token  
**Solution**: Generate a new API token from Canvas Settings

#### 5. "MCP server not found"
**Problem**: Entry point not properly installed  
**Solution**: Re-run `uv sync --extra mcp` and verify installation

#### 6. "Environment variables not loaded"  
**Problem**: MCP client not passing environment variables  
**Solution**: Check MCP client configuration includes `env` section

#### 7. Connection timeouts
**Problem**: Network connectivity issues  
**Solution**: Check network connectivity and Canvas instance availability

### Getting Help

1. **Check server logs** for detailed error messages
2. **Verify Canvas credentials** work in browser
3. **Test Canvas API** with curl command (see Testing section)
4. **Check MCP client logs** for client-specific issues

## Security Notes

⚠️ **Important Security Considerations:**

1. **Keep your API token secure** - treat it like a password
2. **Use environment variables** - never hardcode tokens in files  
3. **Limit token scope** if your Canvas admin allows it
4. **Regenerate tokens periodically** for security
5. **Never commit tokens to version control**
6. **Use HTTPS URLs** for Canvas instances
7. **Validate server logs** don't expose sensitive information

## Performance Tips

1. **Use server-side filtering** with `pandas_operations` to reduce data transfer
2. **Specify `include` parameters** to get only needed related data
3. **Use `limit` parameter** for testing with large datasets
4. **Monitor memory usage** with large Canvas datasets
5. **Consider batch processing** for bulk operations

## Development & Contributing

### Local Development Setup

```bash
# Clone the repository
git clone <repository-url>
cd canvasapi_get

# Install in development mode
uv sync --extra mcp

# Run tests
uv run python test_pandas_operations.py

# Run server in debug mode
uv run canvasapi-mcp --log-level DEBUG
```

### Testing Changes

```bash
# Test entry point
uv run canvasapi-mcp --version

# Test server functionality
export CANVAS_URL="https://test-canvas.instructure.com"
export CANVAS_TOKEN="test-token"
uv run canvasapi-mcp --log-level DEBUG
```

## Version History

- **v0.1.0**: Initial release with 4 MCP tools, server-side filtering, and dynamic method discovery

## Support

For issues, questions, or contributions, please refer to the project documentation and issue tracker.