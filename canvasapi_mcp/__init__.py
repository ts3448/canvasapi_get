"""
Canvas API MCP Server

This module provides MCP (Model Context Protocol) server functionality for the
canvasapi_get library, enabling intelligent Canvas data analysis and querying
through a universal interface.

Key Features:
- Dynamic method resolution for all Canvas API methods
- Universal query tool with parameter validation
- Server-side pandas operations for data filtering
- Seamless integration with existing async infrastructure
- Comprehensive error handling and validation
"""

import asyncio
import sys
from .server import CanvasAPIMCPServer
from .validation import validator, ValidationError
from .tools.canvas_query import CanvasQueryTool
from .tools.method_discovery import MethodDiscoveryTool, MethodInfoTool, PandasOperationsTool
from .resolvers.method_resolver import MethodResolver

__version__ = "0.1.0"
__all__ = [
    "CanvasAPIMCPServer",
    "CanvasQueryTool", 
    "MethodDiscoveryTool",
    "MethodInfoTool",
    "PandasOperationsTool",
    "MethodResolver",
    "validator",
    "ValidationError",
    "main"
]


def main():
    """
    Main entry point for the Canvas API MCP server.
    
    This function is called when the server is started via the command line
    entry point (canvasapi-mcp command). It handles command line arguments
    and starts the MCP server.
    """
    import argparse
    import logging
    
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Canvas API MCP Server",
        prog="canvasapi-mcp"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level (default: INFO)"
    )
    parser.add_argument(
        "--server-name", 
        default="canvas-api",
        help="Name for the MCP server instance (default: canvas-api)"
    )
    parser.add_argument(
        "--canvas-url",
        help="Canvas instance URL (can also be set via CANVAS_URL environment variable)"
    )
    parser.add_argument(
        "--canvas-token",
        help="Canvas API token (can also be set via CANVAS_TOKEN environment variable)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"Canvas API MCP Server {__version__}"
    )
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr)  # MCP uses stdout for protocol communication
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Starting Canvas API MCP Server {__version__}")
    
    try:
        # Create and run the server
        server = CanvasAPIMCPServer(
            canvas_url=args.canvas_url,
            canvas_token=args.canvas_token,
            server_name=args.server_name
        )
        
        # Run the server
        asyncio.run(server.run())
        
    except KeyboardInterrupt:
        logger.info("Server shutting down due to keyboard interrupt")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()