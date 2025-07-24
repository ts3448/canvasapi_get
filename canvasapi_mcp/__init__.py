"""
Canvas API MCP Server

This module provides MCP (Model Context Protocol) server functionality for the
canvasapi_get library, enabling intelligent Canvas data analysis and querying
through a universal interface.

Key Features:
- Dynamic method resolution for all Canvas API methods
- Universal query tool with parameter validation
- Seamless integration with existing async infrastructure
- Comprehensive error handling and validation
"""

from .server import CanvasAPIMCPServer
from .validation import validator, ValidationError
from .tools.canvas_query import CanvasQueryTool
from .tools.method_discovery import MethodDiscoveryTool, MethodInfoTool
from .resolvers.method_resolver import MethodResolver

__version__ = "0.1.0"
__all__ = [
    "CanvasAPIMCPServer",
    "CanvasQueryTool",
    "MethodDiscoveryTool",
    "MethodInfoTool", 
    "MethodResolver",
    "validator",
    "ValidationError"
]