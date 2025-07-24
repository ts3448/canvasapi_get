# Canvas API MCP Server Configuration Examples

This directory contains example configurations for using the Canvas API MCP server with different MCP clients.

## Quick Setup

### 1. Get Your Canvas API Token

1. Log into your Canvas instance
2. Go to **Account** → **Settings** 
3. Scroll to **Approved Integrations**
4. Click **New Access Token**
5. Enter a purpose (e.g., "MCP Server Access")
6. Click **Generate Token**
7. **Copy and save the token immediately** (you won't see it again)

### 2. Configure Your MCP Client

#### For Claude Desktop

1. Find your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the Canvas MCP server configuration:

```json
{
  "mcpServers": {
    "canvas-api": {
      "command": "python",
      "args": ["-m", "canvasapi_mcp.server"],
      "env": {
        "CANVAS_URL": "https://your-school.instructure.com",
        "CANVAS_TOKEN": "your-api-token-here"
      }
    }
  }
}
```

3. Replace:
   - `https://your-school.instructure.com` with your Canvas URL
   - `your-api-token-here` with your actual API token

4. Restart Claude Desktop

#### For Other MCP Clients

Use the appropriate configuration format for your MCP client, ensuring:
- The command runs `python -m canvasapi_mcp.server`
- Environment variables `CANVAS_URL` and `CANVAS_TOKEN` are set
- The Canvas API library is installed in the Python environment

## Environment Variables

The server supports multiple environment variable names for flexibility:

### Canvas URL
- `CANVAS_URL` (recommended)
- `CANVAS_BASE_URL` (alternative)

### Canvas API Token
- `CANVAS_TOKEN` (recommended)
- `CANVAS_API_TOKEN` (alternative)
- `CANVAS_API_KEY` (alternative)

### Optional Settings
- `MCP_SERVER_NAME` (default: "canvas-api")

## Alternative: .env File

You can also create a `.env` file in your project directory:

```bash
CANVAS_URL=https://your-school.instructure.com
CANVAS_TOKEN=your-api-token-here
MCP_SERVER_NAME=canvas-api
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Keep your API token secure** - treat it like a password
2. **Use environment variables** - never hardcode tokens in files
3. **Limit token scope** if your Canvas admin allows it
4. **Regenerate tokens periodically** for security
5. **Never commit tokens to version control**

## Testing Your Configuration

You can test your configuration by running the server directly:

```bash
# Set environment variables
export CANVAS_URL="https://your-school.instructure.com"
export CANVAS_TOKEN="your-api-token-here"

# Run the server
python -m canvasapi_mcp.server
```

The server will perform a health check and report any configuration issues.

## Available Tools

Once configured, the MCP server provides these tools:

1. **`discover_canvas_methods`** - Explore available Canvas API methods
2. **`get_canvas_method_info`** - Get detailed info about specific methods  
3. **`canvas_query`** - Execute Canvas API queries with parameters

## Troubleshooting

### Common Issues

1. **"Canvas URL is required"** - Check your `CANVAS_URL` environment variable
2. **"Canvas API token is required"** - Check your `CANVAS_TOKEN` environment variable
3. **"Failed to resolve"** - Verify your Canvas URL is correct and accessible
4. **"Authentication failed"** - Verify your API token is valid and not expired

### Getting Help

1. Check the server logs for detailed error messages
2. Verify your Canvas credentials work in a browser
3. Test with a simple Canvas API call using curl:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
     "https://your-school.instructure.com/api/v1/users/self"
```

If this works, your credentials are correct and the issue may be with the MCP configuration.