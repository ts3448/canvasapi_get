"""
Tools module for Canvas API MCP integration.

This module contains MCP tools for interacting with the Canvas API,
providing dynamic discovery and universal interface for Canvas operations.
"""

from .canvas_query import CanvasQueryTool
from .method_discovery import MethodDiscoveryTool, MethodInfoTool

__all__ = ["CanvasQueryTool", "MethodDiscoveryTool", "MethodInfoTool"]