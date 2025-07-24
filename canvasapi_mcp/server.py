"""
Canvas API MCP Server

This module provides the main MCP server implementation for Canvas API integration.
It sets up the server with the universal Canvas query tool and handles all
MCP protocol communication with comprehensive error handling.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ListResourcesResult, ListToolsResult, ReadResourceResult, CallToolResult
from canvasapi_get.canvas import Canvas
from canvasapi_get.exceptions import CanvasException
from .tools.canvas_query import CanvasQueryTool
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
    
    def __init__(self, canvas_url: str, canvas_token: str, server_name: str = "canvas-api"):
        """
        Initialize the Canvas API MCP server.
        
        Args:
            canvas_url: Canvas instance URL
            canvas_token: Canvas API token
            server_name: Name for the MCP server
        """
        self.server_name = server_name
        self.canvas = Canvas(canvas_url, canvas_token)
        self.query_tool = CanvasQueryTool(self.canvas)
        self.method_resolver = MethodResolver(self.canvas)
        
        # Initialize MCP server
        self.server = Server(server_name)
        self._setup_handlers()
    
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
            tools = [self.query_tool.get_tool_definition()]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            """Handle tool calls."""
            try:
                if name == "canvas_query":
                    result = await self.query_tool.execute(arguments)
                    return CallToolResult(content=result)
                else:
                    error_content = [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
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
    
    def get_server_info(self) -> Dict[str, Any]:
        """
        Get information about the server configuration.
        
        Returns:
            Dictionary containing server information
        """
        return {
            "server_name": self.server_name,
            "canvas_url": self.canvas.base_url,
            "available_tools": ["canvas_query"],
            "supported_object_types": self.method_resolver.get_available_object_types(),
            "version": "0.1.0"
        }
    
    async def health_check(self) -> Dict[str, Any]:
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


def create_server(canvas_url: str, canvas_token: str, server_name: str = "canvas-api") -> CanvasAPIMCPServer:
    """
    Factory function to create a Canvas API MCP server.
    
    Args:
        canvas_url: Canvas instance URL
        canvas_token: Canvas API token  
        server_name: Name for the MCP server
        
    Returns:
        Configured CanvasAPIMCPServer instance
    """
    return CanvasAPIMCPServer(canvas_url, canvas_token, server_name)


async def main():
    """
    Main entry point for running the server as a standalone application.
    
    This function expects environment variables:
    - CANVAS_URL: Canvas instance URL
    - CANVAS_TOKEN: Canvas API token
    """
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    canvas_url = os.getenv("CANVAS_URL")
    canvas_token = os.getenv("CANVAS_TOKEN")
    server_name = os.getenv("MCP_SERVER_NAME", "canvas-api")
    
    if not canvas_url or not canvas_token:
        raise ValueError("CANVAS_URL and CANVAS_TOKEN environment variables are required")
    
    # Create and run server
    server = create_server(canvas_url, canvas_token, server_name)
    
    # Perform health check
    health = await server.health_check()
    logger.info(f"Server health check: {health}")
    
    if health["status"] != "healthy":
        logger.error("Server health check failed, but continuing...")
    
    # Run the server
    await server.run()


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the server
    asyncio.run(main())