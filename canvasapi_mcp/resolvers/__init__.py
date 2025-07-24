"""
Resolvers module for Canvas API method resolution.

This module contains components for dynamically discovering and resolving
Canvas API methods for MCP tool invocation.
"""

from .method_resolver import MethodResolver

__all__ = ["MethodResolver"]