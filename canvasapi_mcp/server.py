"""
Canvas API MCP Server

This module provides the main MCP server implementation for Canvas API integration.
It sets up the server with the universal Canvas query tool and handles all
MCP protocol communication with comprehensive error handling.
"""

import asyncio
import logging
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ListResourcesResult, ListToolsResult, ReadResourceResult, CallToolResult
from canvasapi_get.canvas import Canvas
from canvasapi_get.exceptions import CanvasException
from .tools.canvas_query import CanvasQueryTool
from .tools.method_discovery import MethodDiscoveryTool, MethodInfoTool, PandasOperationsTool
from .resolvers.method_resolver import MethodResolver
from .validation import ValidationError

# Configure logging
logger = logging.getLogger(__name__)


class CanvasAPIMCPServer:
    """
    MCP Server for Canvas API integration.
    
    This server provides a universal interface to the Canvas API through MCP,
    allowing clients to query Canvas data using natural language through
    the dynamic method resolution system.
    """
    
    def __init__(self, canvas_url: str | None = None, canvas_token: str | None = None, server_name: str = "canvas-api"):
        """
        Initialize the Canvas API MCP server.
        
        Args:
            canvas_url: Canvas instance URL (can be None to read from environment)
            canvas_token: Canvas API token (can be None to read from environment)
            server_name: Name for the MCP server
        """
        self.server_name = server_name
        
        # Load configuration from environment if not provided
        self.canvas_url, self.canvas_token = self._load_configuration(canvas_url, canvas_token)
        
        # Initialize Canvas API connection
        self.canvas = Canvas(self.canvas_url, self.canvas_token)
        
        # Initialize tools
        self.query_tool = CanvasQueryTool(self.canvas)
        self.discovery_tool = MethodDiscoveryTool(self.canvas)
        self.method_info_tool = MethodInfoTool(self.canvas)
        self.pandas_operations_tool = PandasOperationsTool(self.canvas)
        self.method_resolver = MethodResolver(self.canvas)
        
        # Initialize MCP server
        self.server = Server(server_name)
        self._setup_handlers()
    
    def _load_configuration(self, canvas_url: str | None, canvas_token: str | None) -> tuple[str, str]:
        """
        Load Canvas configuration from parameters or environment variables.
        
        Args:
            canvas_url: Provided Canvas URL (optional)
            canvas_token: Provided Canvas token (optional)
            
        Returns:
            Tuple of (canvas_url, canvas_token)
            
        Raises:
            ValueError: If configuration cannot be loaded
        """
        import os
        
        # Try provided parameters first, then environment variables
        final_url = canvas_url or os.getenv("CANVAS_URL") or os.getenv("CANVAS_BASE_URL")
        final_token = canvas_token or os.getenv("CANVAS_TOKEN") or os.getenv("CANVAS_API_TOKEN") or os.getenv("CANVAS_API_KEY")
        
        # Validate required configuration
        if not final_url:
            raise ValueError(
                "Canvas URL is required. Provide it via:\n"
                "1. CANVAS_URL environment variable\n" 
                "2. CANVAS_BASE_URL environment variable\n"
                "3. canvas_url parameter\n"
                "Example: CANVAS_URL=https://your-school.instructure.com"
            )
        
        if not final_token:
            raise ValueError(
                "Canvas API token is required. Provide it via:\n"
                "1. CANVAS_TOKEN environment variable\n"
                "2. CANVAS_API_TOKEN environment variable\n" 
                "3. CANVAS_API_KEY environment variable\n"
                "4. canvas_token parameter\n"
                "Get your token from Canvas: Account → Settings → Approved Integrations → New Access Token"
            )
        
        # Normalize URL (ensure https and remove trailing slash)
        if not final_url.startswith(('http://', 'https://')):
            final_url = f"https://{final_url}"
        final_url = final_url.rstrip('/')
        
        logger.info(f"Canvas MCP Server configured for: {final_url}")
        return final_url, final_token
    
    def _setup_handlers(self):
        """Set up MCP protocol handlers."""
        
        @self.server.list_resources()
        async def list_resources() -> ListResourcesResult:
            """List available resources."""
            resources = [
                Resource(
                    uri="canvas://methods",
                    name="Available Canvas Methods",
                    description="List of all available Canvas API methods by object type",
                    mimeType="application/json"
                ),
                Resource(
                    uri="canvas://object-types", 
                    name="Canvas Object Types",
                    description="List of supported Canvas object types for queries",
                    mimeType="application/json"
                )
            ]
            return ListResourcesResult(resources=resources)
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> ReadResourceResult:
            """Read a specific resource."""
            try:
                if uri == "canvas://methods":
                    # Get all available methods for Canvas object
                    methods = self.method_resolver.discover_methods(self.canvas)
                    content = {
                        "canvas_methods": methods,
                        "description": "Available methods on the main Canvas object"
                    }
                    return ReadResourceResult(
                        contents=[TextContent(
                            type="text",
                            text=str(content)
                        )]
                    )
                
                elif uri == "canvas://object-types":
                    object_types = self.method_resolver.get_available_object_types()
                    content = {
                        "supported_object_types": object_types,
                        "description": "Canvas object types that can be queried"
                    }
                    return ReadResourceResult(
                        contents=[TextContent(
                            type="text", 
                            text=str(content)
                        )]
                    )
                
                else:
                    return ReadResourceResult(
                        contents=[TextContent(
                            type="text",
                            text=f"Resource not found: {uri}"
                        )]
                    )
                    
            except Exception as e:
                logger.error(f"Error reading resource {uri}: {str(e)}")
                return ReadResourceResult(
                    contents=[TextContent(
                        type="text",
                        text=f"Error reading resource: {str(e)}"
                    )]
                )
        
        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            """List available tools."""
            tools = [
                self.discovery_tool.get_tool_definition(),
                self.method_info_tool.get_tool_definition(),
                self.pandas_operations_tool.get_tool_definition(),
                self.query_tool.get_tool_definition()
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> CallToolResult:
            """Handle tool calls."""
            try:
                if name == "discover_canvas_methods":
                    result = await self.discovery_tool.execute(arguments)
                    return CallToolResult(content=result)
                elif name == "get_canvas_method_info":
                    result = await self.method_info_tool.execute(arguments)
                    return CallToolResult(content=result)
                elif name == "get_pandas_operations":
                    result = await self.pandas_operations_tool.execute(arguments)
                    return CallToolResult(content=result)
                elif name == "canvas_query":
                    result = await self.query_tool.execute(arguments)
                    return CallToolResult(content=result)
                else:
                    error_content = [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}. Available tools: discover_canvas_methods, get_canvas_method_info, get_pandas_operations, canvas_query"
                    )]
                    return CallToolResult(content=error_content)
                    
            except Exception as e:
                logger.error(f"Error calling tool {name}: {str(e)}")
                error_content = [TextContent(
                    type="text",
                    text=f"Tool execution error: {str(e)}"
                )]
                return CallToolResult(content=error_content)
    
    async def run(self, transport_type: str = "stdio", **transport_kwargs):
        """
        Run the MCP server.
        
        Args:
            transport_type: Type of transport ("stdio", "sse", etc.)
            **transport_kwargs: Additional transport-specific arguments
        """
        try:
            logger.info(f"Starting Canvas API MCP server: {self.server_name}")
            
            if transport_type == "stdio":
                from mcp.server.stdio import stdio_server
                async with stdio_server() as (read_stream, write_stream):
                    await self.server.run(
                        read_stream, 
                        write_stream,
                        self.server.create_initialization_options()
                    )
            else:
                raise ValueError(f"Unsupported transport type: {transport_type}")
                
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            raise
    
    def get_server_info(self) -> dict[str, str | list[str]]:
        """
        Get information about the server configuration.
        
        Returns:
            Dictionary containing server information
        """
        return {
            "server_name": self.server_name,
            "canvas_url": self.canvas_url,
            "available_tools": ["discover_canvas_methods", "get_canvas_method_info", "get_pandas_operations", "canvas_query"],
            "supported_object_types": self.method_resolver.get_available_object_types(),
            "version": "0.1.0"
        }
    
    async def health_check(self) -> dict:
        """
        Perform a health check on the server and Canvas connection.
        
        Returns:
            Dictionary containing health status
        """
        try:
            # Test Canvas connection with a simple API call
            user = self.canvas.get_current_user()
            
            return {
                "status": "healthy",
                "canvas_connection": "ok",
                "current_user": {
                    "id": getattr(user, 'id', None),
                    "name": getattr(user, 'name', None)
                },
                "server_info": self.get_server_info()
            }
            
        except CanvasException as e:
            return {
                "status": "unhealthy",
                "canvas_connection": "failed",
                "error": str(e),
                "server_info": self.get_server_info()
            }
        except Exception as e:
            return {
                "status": "unhealthy", 
                "canvas_connection": "unknown",
                "error": str(e),
                "server_info": self.get_server_info()
            }
    
    def clear_caches(self):
        """Clear all internal caches."""
        self.method_resolver.clear_cache()
        logger.info("Server caches cleared")


def create_server(canvas_url: str | None = None, canvas_token: str | None = None, server_name: str = "canvas-api") -> CanvasAPIMCPServer:
    """
    Factory function to create a Canvas API MCP server.
    
    Args:
        canvas_url: Canvas instance URL (optional, reads from environment if not provided)
        canvas_token: Canvas API token (optional, reads from environment if not provided)
        server_name: Name for the MCP server
        
    Returns:
        Configured CanvasAPIMCPServer instance
    """
    return CanvasAPIMCPServer(canvas_url, canvas_token, server_name)


async def main():
    """
    Main entry point for running the server as a standalone application.
    
    This function reads configuration from environment variables:
    - CANVAS_URL or CANVAS_BASE_URL: Canvas instance URL
    - CANVAS_TOKEN, CANVAS_API_TOKEN, or CANVAS_API_KEY: Canvas API token
    - MCP_SERVER_NAME: Optional server name (defaults to "canvas-api")
    """
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    server_name = os.getenv("MCP_SERVER_NAME", "canvas-api")
    
    try:
        # Create server (will read config from environment automatically)
        server = create_server(server_name=server_name)
        
        # Perform health check
        health = await server.health_check()
        logger.info(f"Server health check: {health}")
        
        if health["status"] != "healthy":
            logger.error("Server health check failed, but continuing...")
        
        # Run the server
        await server.run()
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise
    except Exception as e:
        logger.error(f"Server startup error: {e}")
        raise


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the server
    asyncio.run(main())