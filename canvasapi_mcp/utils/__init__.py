"""
Utilities module for Canvas API MCP integration.

This module contains utility functions and classes for MCP server functionality,
including DataFrame conversion, pandas operations, and attribute discovery.
"""

# Phase 2 imports:
from .dataframe_converter import DataFrameConverter, converter, convert_to_dataframe, get_dataframe_info
from .attribute_discovery import AttributeDiscovery

# Future imports for Phase 3+:
# from .pandas_engine import PandasEngine

__all__ = [
    "DataFrameConverter",
    "converter", 
    "convert_to_dataframe",
    "get_dataframe_info",
    "AttributeDiscovery"
]