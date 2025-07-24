"""
Universal Canvas API query tool for MCP server.

This module provides a generic tool that can call any Canvas API method
dynamically through the MCP protocol, with comprehensive parameter validation
and error handling.
"""

import json
from typing import Any, Dict, List, Optional, Union
from mcp.types import Tool, TextContent
from canvasapi_get.canvas import Canvas
from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.paginated_list import PaginatedList
from canvasapi_get.exceptions import CanvasException
from ..resolvers.method_resolver import MethodResolver, MethodResolutionError
from ..validation import validator, ValidationError


class CanvasQueryTool:
    """
    Universal Canvas API query tool for MCP integration.
    
    This tool provides a single interface for calling any Canvas API method
    by specifying the target object type, method name, and parameters.
    It handles dynamic method resolution, parameter validation, and response
    formatting automatically.
    """
    
    def __init__(self, canvas: Canvas):
        """
        Initialize the Canvas query tool.
        
        Args:
            canvas: Canvas API instance for method execution
        """
        self.canvas = canvas
        self.resolver = MethodResolver(canvas)
    
    def get_tool_definition(self) -> Tool:
        """
        Get the MCP tool definition for the Canvas query tool.
        
        Returns:
            MCP Tool definition
        """
        return Tool(
            name="canvas_query",
            description="""
            Universal Canvas API query tool that can call any Canvas GET method dynamically.
            
            This tool allows you to:
            - Call any Canvas API method on any object type
            - Retrieve courses, users, assignments, etc. with full parameter support
            - Chain method calls (e.g., get assignment from specific course)
            - Handle pagination automatically
            - Get comprehensive error information
            
            Examples:
            - Get course: {"object_type": "canvas", "method": "get_course", "parameters": {"course_id": 12345}}
            - Get course assignments: {"object_type": "course", "object_id": 12345, "method": "get_assignments"}
            - Get user with includes: {"object_type": "canvas", "method": "get_user", "parameters": {"user_id": 678, "include": ["enrollments"]}}
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "object_type": {
                        "type": "string",
                        "description": "Type of Canvas object (canvas, course, user, assignment, etc.)",
                        "enum": [
                            "canvas", "account", "course", "user", "group", "section",
                            "enrollment_term", "external_tool", "assignment", "discussion_topic",
                            "quiz", "module", "page", "file", "folder", "enrollment",
                            "calendar_event", "submission", "rubric"
                        ]
                    },
                    "object_id": {
                        "type": ["integer", "string"],
                        "description": "Canvas object ID (not needed for 'canvas' object_type)"
                    },
                    "method": {
                        "type": "string", 
                        "description": "Canvas method to call (e.g., 'get_courses', 'get_assignments', 'get_users')"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Parameters to pass to the Canvas method",
                        "additionalProperties": True
                    },
                    "object_chain": {
                        "type": "array",
                        "description": "For chained calls, array of objects to traverse",
                        "items": {
                            "type": "object",
                            "properties": {
                                "object_type": {"type": "string"},
                                "object_id": {"type": ["integer", "string"]}
                            },
                            "required": ["object_type", "object_id"]
                        }
                    },
                    "output_format": {
                        "type": "string",
                        "description": "Output format preference",
                        "enum": ["json", "summary", "count"],
                        "default": "json"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Limit number of results (for paginated responses)",
                        "minimum": 1,
                        "maximum": 1000
                    }
                },
                "required": ["object_type", "method"],
                "additionalProperties": False
            }
        )
    
    async def execute(self, arguments: Dict[str, Any]) -> List[TextContent]:
        """
        Execute a Canvas API query with the provided arguments.
        
        Args:
            arguments: Tool arguments from MCP request
            
        Returns:
            List of TextContent responses
        """
        try:
            # Extract and validate arguments
            object_type = arguments.get("object_type")
            object_id = arguments.get("object_id")
            method_name = arguments.get("method")
            parameters = arguments.get("parameters", {})
            object_chain = arguments.get("object_chain")
            output_format = arguments.get("output_format", "json")
            limit = arguments.get("limit")
            
            # Validate required arguments
            if not object_type or not method_name:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "missing_required_arguments",
                        "message": "object_type and method are required"
                    }, indent=2)
                )]
            
            # Validate object_id requirement
            if object_type.lower() != "canvas" and not object_id and not object_chain:
                return [TextContent(
                    type="text", 
                    text=json.dumps({
                        "error": "missing_object_id",
                        "message": f"object_id is required for object_type '{object_type}'"
                    }, indent=2)
                )]
            
            # Execute the method call
            if object_chain:
                result = self.resolver.resolve_chained_method_call(
                    object_chain, method_name, parameters
                )
            else:
                result = self.resolver.resolve_method_call(
                    object_type, object_id, method_name, parameters
                )
            
            # Format the response
            formatted_result = self._format_result(result, output_format, limit)
            
            return [TextContent(
                type="text",
                text=json.dumps(formatted_result, indent=2, default=str)
            )]
            
        except MethodResolutionError as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "method_resolution_error",
                    "message": str(e)
                }, indent=2)
            )]
            
        except ValidationError as e:
            return [TextContent(
                type="text",
                text=json.dumps(validator.format_validation_error(e), indent=2)
            )]
            
        except CanvasException as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "canvas_api_error",
                    "message": str(e),
                    "error_code": getattr(e, 'error_code', None)
                }, indent=2)
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "unexpected_error",
                    "message": str(e),
                    "type": type(e).__name__
                }, indent=2)
            )]
    
    def _format_result(self, result: Any, output_format: str, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Format the Canvas API result for MCP response.
        
        Args:
            result: Canvas API result
            output_format: Desired output format
            limit: Optional result limit
            
        Returns:
            Formatted result dictionary
        """
        try:
            # Handle different result types
            if isinstance(result, PaginatedList):
                return self._format_paginated_result(result, output_format, limit)
            elif isinstance(result, CanvasObject):
                return self._format_canvas_object(result, output_format)
            elif isinstance(result, list):
                return self._format_list_result(result, output_format, limit)
            else:
                # Primitive result (string, int, bool, etc.)
                return {
                    "success": True,
                    "result_type": "primitive",
                    "data": result,
                    "format": output_format
                }
                
        except Exception as e:
            return {
                "error": "formatting_error",
                "message": f"Failed to format result: {str(e)}",
                "raw_result_type": type(result).__name__
            }
    
    def _format_paginated_result(self, paginated_list: PaginatedList, output_format: str, limit: Optional[int]) -> Dict[str, Any]:
        """Format PaginatedList results."""
        items = []
        count = 0
        
        try:
            for item in paginated_list:
                if limit and count >= limit:
                    break
                items.append(item)
                count += 1
        except Exception as e:
            return {
                "error": "pagination_error",
                "message": f"Error reading paginated results: {str(e)}",
                "partial_count": count
            }
        
        if output_format == "count":
            return {
                "success": True,
                "result_type": "paginated_count",
                "count": count,
                "limited": limit is not None and count >= limit
            }
        elif output_format == "summary":
            return {
                "success": True,
                "result_type": "paginated_summary", 
                "count": count,
                "limited": limit is not None and count >= limit,
                "sample_items": [self._object_to_dict(item) for item in items[:5]]
            }
        else:  # json format
            return {
                "success": True,
                "result_type": "paginated_list",
                "count": count,
                "limited": limit is not None and count >= limit,
                "data": [self._object_to_dict(item) for item in items]
            }
    
    def _format_canvas_object(self, obj: CanvasObject, output_format: str) -> Dict[str, Any]:
        """Format single CanvasObject results."""
        if output_format == "count":
            return {
                "success": True,
                "result_type": "single_object_count",
                "count": 1
            }
        elif output_format == "summary":
            obj_dict = self._object_to_dict(obj)
            # Create summary with key fields
            summary_fields = ['id', 'name', 'title', 'code', 'email', 'login_id']
            summary = {k: v for k, v in obj_dict.items() if k in summary_fields and v is not None}
            return {
                "success": True,
                "result_type": "single_object_summary",
                "object_type": type(obj).__name__,
                "summary": summary
            }
        else:  # json format
            return {
                "success": True,
                "result_type": "single_object",
                "object_type": type(obj).__name__,
                "data": self._object_to_dict(obj)
            }
    
    def _format_list_result(self, result_list: List[Any], output_format: str, limit: Optional[int]) -> Dict[str, Any]:
        """Format regular list results."""
        items = result_list[:limit] if limit else result_list
        
        if output_format == "count":
            return {
                "success": True,
                "result_type": "list_count",
                "count": len(items),
                "total_count": len(result_list),
                "limited": limit is not None and len(result_list) > limit
            }
        elif output_format == "summary":
            return {
                "success": True,
                "result_type": "list_summary",
                "count": len(items),
                "total_count": len(result_list),
                "limited": limit is not None and len(result_list) > limit,
                "sample_items": [self._object_to_dict(item) for item in items[:5]]
            }
        else:  # json format
            return {
                "success": True,
                "result_type": "list",
                "count": len(items),
                "total_count": len(result_list),
                "limited": limit is not None and len(result_list) > limit,
                "data": [self._object_to_dict(item) for item in items]
            }
    
    def _object_to_dict(self, obj: Any) -> Any:
        """Convert Canvas object to dictionary representation."""
        if isinstance(obj, CanvasObject):
            return validator.convert_canvas_object_to_dict(obj)
        elif hasattr(obj, '__dict__'):
            # Generic object with attributes
            return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}
        else:
            # Primitive value
            return obj
    
    def get_available_methods(self, object_type: str, object_id: Optional[Union[int, str]] = None) -> List[Dict[str, Any]]:
        """
        Get list of available methods for a Canvas object type.
        
        Args:
            object_type: Type of Canvas object
            object_id: Optional object ID for instance-specific methods
            
        Returns:
            List of available method information
        """
        try:
            if object_type.lower() == "canvas":
                return self.resolver.discover_methods(self.canvas)
            elif object_id:
                obj = self.resolver.resolve_canvas_object(object_type, object_id)
                return self.resolver.discover_methods(obj)
            else:
                # Return class-level methods without instance
                return []
        except Exception as e:
            return [{"error": f"Failed to discover methods: {str(e)}"}]