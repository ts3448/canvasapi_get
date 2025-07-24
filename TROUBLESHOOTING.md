# Canvas API MCP Server - Troubleshooting Guide

## Issue: MCP Server Shows as Disabled with No Tools

If your MCP server appears as disabled in Claude Desktop or shows no tools available, follow these troubleshooting steps:

### ✅ **RESOLVED: Python Syntax & Type Errors**

**Issues Fixed**:
1. **JavaScript-style boolean literals**: Had `false`, `true` instead of Python literals (`False`, `True`)
2. **MCP type mismatch**: Used `TextContent` instead of `TextResourceContents` for resource reading
3. **Missing uri parameter**: TextResourceContents required uri parameter and proper mimeType

**Status**: ✅ **All fixed and verified working**

1. **Update the server code** by pulling the latest changes
2. **Restart Claude Desktop** after updating
3. **Verify the fix** by running the test script:
   ```bash
   cd /path/to/canvasapi_get
   uv run python test_mcp_server.py
   ```

### Common Troubleshooting Steps

#### 1. Verify Server Installation

```bash
cd /path/to/canvasapi_get
uv sync --extra mcp
uv run canvasapi-mcp --version
# Should output: Canvas API MCP Server 0.1.0
```

#### 2. Test Server Functionality

```bash
# Run the server test script
uv run python test_mcp_server.py
```

This should show all 4 tools are properly defined:
- `discover_canvas_methods`
- `get_canvas_method_info` 
- `get_pandas_operations`
- `canvas_query`

#### 3. Check Claude Desktop Configuration

Ensure your `claude_desktop_config.json` has the correct configuration:

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

**Important**:
- Use **absolute paths** (not relative paths like `~/` or `./`)
- Replace `/absolute/path/to/canvasapi_get` with your actual project path
- Replace Canvas URL and token with your actual values

#### 4. Restart Claude Desktop

After making configuration changes:
1. **Quit Claude Desktop completely**
2. **Wait 5 seconds**
3. **Restart Claude Desktop**

#### 5. Check MCP Logs (if available)

If Claude Desktop has developer mode enabled:
1. Look for MCP logs in Claude Desktop
2. Check for any error messages related to `canvas-api` server
3. Look for connection or startup errors

#### 6. Test Server Manually

Test the server startup manually:

```bash
# Set environment variables
export CANVAS_URL="https://your-school.instructure.com"
export CANVAS_TOKEN="your-api-token-here"

# Run server with debug logging
cd /absolute/path/to/canvasapi_get
uv run canvasapi-mcp --log-level DEBUG
```

The server should start and wait for MCP client connections. Look for:
- ✅ "Starting Canvas API MCP Server 0.1.0"
- ✅ "Canvas MCP Server configured for: [your-url]"
- ✅ No error messages about missing tools or configuration

### Configuration Issues

#### Wrong Path Format
❌ **Bad**: `"~/Documents/canvasapi_get"`
❌ **Bad**: `"./canvasapi_get"`
✅ **Good**: `"/Users/username/Documents/canvasapi_get"`

#### Missing Dependencies
If you see "No module named 'mcp'" or similar:
```bash
uv sync --extra mcp
```

#### Wrong Canvas URL Format
❌ **Bad**: `"myschool.instructure.com"`
✅ **Good**: `"https://myschool.instructure.com"`

#### Environment Variables Not Set
The server requires both `CANVAS_URL` and `CANVAS_TOKEN`. If these aren't in your MCP config `env` section, the server will fail to start.

### Testing Your Setup

#### 1. Verify Canvas Credentials
Test your Canvas credentials work:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://your-school.instructure.com/api/v1/users/self"
```

#### 2. Test MCP Server Health
```bash
export CANVAS_URL="https://your-school.instructure.com"
export CANVAS_TOKEN="your-api-token-here"
cd /absolute/path/to/canvasapi_get
uv run python test_mcp_server.py
```

Should show:
- ✅ Server created successfully
- ✅ All 4 tools properly defined
- ✅ Method resolver working
- ⚠️ Health check may fail if Canvas URL is unreachable (this is OK for testing)

#### 3. Verify uv and Python Environment
```bash
which uv
# Should show path to uv

uv --version
# Should show uv version

cd /absolute/path/to/canvasapi_get
uv run python --version
# Should show Python 3.10+
```

### Known Issues and Solutions

#### Issue: "Server shows as disabled"
**Cause**: Usually due to configuration errors or failed server startup  
**Solution**: Check Claude Desktop logs and verify configuration

#### Issue: "No tools available"
**Cause**: Server started but tools aren't being registered properly  
**Solution**: This was caused by Python syntax errors (now fixed)

#### Issue: "Connection timeout"
**Cause**: Network issues or incorrect Canvas URL  
**Solution**: Verify Canvas URL is accessible and credentials are valid

#### Issue: "Permission denied"
**Cause**: File permissions or path issues  
**Solution**: Ensure paths are correct and files are executable

### Getting Additional Help

1. **Run the test script**: `uv run python test_mcp_server.py`
2. **Check the logs**: Look for error messages in server output
3. **Verify configuration**: Double-check all paths and credentials
4. **Test Canvas API**: Verify credentials work with curl
5. **Restart everything**: Restart Claude Desktop after any changes

### Success Indicators

When everything is working correctly, you should see:

1. **In Claude Desktop**: Canvas API server appears as enabled with 4 tools available
2. **In server logs**: No error messages, successful startup
3. **In test script**: All components show as working correctly

The server provides these tools once properly configured:
- **discover_canvas_methods** - Explore Canvas API
- **get_canvas_method_info** - Get method details  
- **get_pandas_operations** - Server-side filtering
- **canvas_query** - Execute Canvas queries with filtering