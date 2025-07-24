"""
Canvas API method discovery tool for MCP server.

This tool allows clients to dynamically discover available methods on Canvas
objects, enabling intelligent exploration of the Canvas API structure without
hardcoded mappings.
"""

import json
from mcp.types import Tool, TextContent
from canvasapi_get.canvas import Canvas
from canvasapi_get.canvas_object import CanvasObject
from ..resolvers.method_resolver import MethodResolver, MethodResolutionError


class MethodDiscoveryTool:
    """
    Canvas API method discovery tool for MCP integration.
    
    This tool enables clients to dynamically explore the Canvas API by
    discovering what methods are available on any Canvas object type,
    allowing for intelligent API navigation and understanding.
    """
    
    def __init__(self, canvas: Canvas):
        """
        Initialize the method discovery tool.
        
        Args:
            canvas: Canvas API instance for method discovery
        """
        self.canvas = canvas
        self.resolver = MethodResolver(canvas)
    
    def get_tool_definition(self) -> Tool:
        """
        Get the MCP tool definition for method discovery.
        
        Returns:
            MCP Tool definition
        """
        return Tool(
            name="discover_canvas_methods",
            description="""
            Discover available methods on Canvas API objects dynamically.
            
            This tool allows you to explore the Canvas API structure by discovering
            what methods are available on different object types. Use this to understand
            the Canvas API capabilities and plan your method calls.
            
            Examples:
            - Discover Canvas main methods: {"object_type": "canvas"}
            - Discover Course methods: {"object_type": "course", "sample_id": 12345}
            - Discover User methods: {"object_type": "user", "sample_id": 67890}
            - Filter by prefix: {"object_type": "canvas", "method_prefix": "get_"}
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "object_type": {
                        "type": "string",
                        "description": "Type of Canvas object to explore (canvas, course, user, account, etc.)",
                        "enum": [
                            "canvas", "account", "course", "user", "group", "section",
                            "enrollment_term", "external_tool", "assignment", "discussion_topic",
                            "quiz", "module", "page", "file", "folder", "enrollment",
                            "calendar_event", "submission", "rubric"
                        ]
                    },
                    "sample_id": {
                        "type": ["integer", "string"],
                        "description": "Sample object ID for discovering instance methods (not needed for 'canvas' type)"
                    },
                    "method_prefix": {
                        "type": "string",
                        "description": "Filter methods by prefix (e.g., 'get_', 'list_')"
                    },
                    "include_details": {
                        "type": "boolean",
                        "description": "Include detailed parameter information for each method",
                        "default": false
                    }
                },
                "required": ["object_type"],
                "additionalProperties": false
            }
        )
    
    async def execute(self, arguments: dict) -> list[TextContent]:
        """
        Execute method discovery with the provided arguments.
        
        Args:
            arguments: Tool arguments from MCP request
            
        Returns:
            List of TextContent responses
        """
        try:
            # Extract and validate arguments
            object_type = arguments.get("object_type")
            sample_id = arguments.get("sample_id")
            method_prefix = arguments.get("method_prefix", "")
            include_details = arguments.get("include_details", False)
            
            # Validate required arguments
            if not object_type:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "missing_required_arguments",
                        "message": "object_type is required"
                    }, indent=2)
                )]
            
            # Get the target object for method discovery
            target_obj = self._get_discovery_target(object_type, sample_id)
            
            # Discover methods
            methods = self.resolver.discover_methods(target_obj, method_prefix)
            
            # Format response
            result = {
                "success": True,
                "object_type": object_type,
                "method_count": len(methods),
                "methods": methods if include_details else [m["name"] for m in methods],
                "discovery_info": {
                    "prefix_filter": method_prefix or "none",
                    "include_details": include_details,
                    "sample_id_used": sample_id if sample_id else "none"
                }
            }
            
            if not include_details:
                result["note"] = "Use include_details=true for parameter information, or use get_canvas_method_info for specific methods"
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
            
        except MethodResolutionError as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "method_discovery_error",
                    "message": str(e)
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
    
    def _get_discovery_target(self, object_type: str, sample_id: int | str | None):
        """
        Get the target object for method discovery.
        
        Args:
            object_type: Type of Canvas object
            sample_id: Optional sample ID for object resolution
            
        Returns:
            Target object for method discovery
            
        Raises:
            MethodResolutionError: If target cannot be resolved
        """
        if object_type.lower() == "canvas":
            return self.canvas
        
        # For other object types, we need a sample instance or class inspection
        if sample_id:
            try:
                return self.resolver.resolve_canvas_object(object_type, sample_id)
            except MethodResolutionError:
                # If we can't resolve with the sample ID, fall back to class inspection
                pass
        
        # Fall back to class-level inspection
        # This is trickier since we need the class, not an instance
        try:
            # Map object types to Canvas methods that return instances
            canvas_method_map = {
                "account": "get_account",
                "course": "get_course", 
                "user": "get_user",
                "group": "get_group",
                "section": "get_section",
                "enrollment_term": "get_enrollment_term",
                "external_tool": "get_external_tool"
            }
            
            method_name = canvas_method_map.get(object_type.lower())
            if method_name and hasattr(self.canvas, method_name):
                # Get the method and try to inspect its return type class
                method = getattr(self.canvas, method_name)
                # This is a bit hacky, but we can try to get the class from method annotations
                # or fall back to generic method discovery
                
                # For now, return a generic representation that we can discover methods from
                # In a real implementation, we might want to use a factory or registry
                raise MethodResolutionError(
                    f"Cannot discover methods for {object_type} without a sample_id. "
                    f"Please provide a sample_id for instance method discovery."
                )
            else:
                raise MethodResolutionError(f"Unknown object type: {object_type}")
                
        except Exception as e:
            raise MethodResolutionError(f"Failed to get discovery target for {object_type}: {str(e)}")


class MethodInfoTool:
    """
    Canvas API method information tool for MCP integration.
    
    This tool provides detailed information about specific Canvas API methods,
    including parameters, types, and documentation.
    """
    
    def __init__(self, canvas: Canvas):
        """
        Initialize the method info tool.
        
        Args:
            canvas: Canvas API instance for method inspection
        """
        self.canvas = canvas
        self.resolver = MethodResolver(canvas)
    
    def get_tool_definition(self) -> Tool:
        """
        Get the MCP tool definition for method info.
        
        Returns:
            MCP Tool definition
        """
        return Tool(
            name="get_canvas_method_info",
            description="""
            Get detailed information about a specific Canvas API method.
            
            Use this tool to understand how to call specific Canvas methods,
            including required parameters, optional parameters, and return types.
            
            Examples:
            - Get info about Canvas.get_course: {"object_type": "canvas", "method_name": "get_course"}
            - Get info about Course.get_assignments: {"object_type": "course", "method_name": "get_assignments"}
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "object_type": {
                        "type": "string",
                        "description": "Type of Canvas object that has the method",
                        "enum": [
                            "canvas", "account", "course", "user", "group", "section",
                            "enrollment_term", "external_tool", "assignment", "discussion_topic",
                            "quiz", "module", "page", "file", "folder", "enrollment",
                            "calendar_event", "submission", "rubric"
                        ]
                    },
                    "method_name": {
                        "type": "string",
                        "description": "Name of the method to get information about"
                    },
                    "sample_id": {
                        "type": ["integer", "string"],
                        "description": "Sample object ID for method inspection (not needed for 'canvas' type)"
                    }
                },
                "required": ["object_type", "method_name"],
                "additionalProperties": false
            }
        )
    
    async def execute(self, arguments: dict) -> list[TextContent]:
        """
        Execute method info retrieval with the provided arguments.
        
        Args:
            arguments: Tool arguments from MCP request
            
        Returns:
            List of TextContent responses
        """
        try:
            # Extract and validate arguments
            object_type = arguments.get("object_type")
            method_name = arguments.get("method_name")
            sample_id = arguments.get("sample_id")
            
            # Validate required arguments
            if not object_type or not method_name:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "error": "missing_required_arguments",
                        "message": "object_type and method_name are required"
                    }, indent=2)
                )]
            
            # Get method information
            method_info = self.resolver.get_method_info(object_type, method_name)
            
            # Enhanced response format
            result = {
                "success": True,
                "object_type": object_type,
                "method_name": method_name,
                "method_info": method_info,
                "usage_example": self._generate_usage_example(object_type, method_name, method_info)
            }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
            
        except MethodResolutionError as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "method_info_error",
                    "message": str(e)
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
    
    def _generate_usage_example(self, object_type: str, method_name: str, method_info: dict) -> dict:
        """
        Generate a usage example for the canvas_query tool.
        
        Args:
            object_type: Canvas object type
            method_name: Method name
            method_info: Method information dictionary
            
        Returns:
            Dictionary containing usage example
        """
        example = {
            "tool": "canvas_query",
            "arguments": {
                "object_type": object_type,
                "method": method_name
            }
        }
        
        # Add object_id if not canvas type
        if object_type.lower() != "canvas":
            example["arguments"]["object_id"] = "YOUR_OBJECT_ID"
        
        # Add parameter examples if available
        if "parameters" in method_info and method_info["parameters"]:
            example_params = {}
            for param_name, param_info in method_info["parameters"].items():
                if param_info.get("required", False):
                    example_params[param_name] = f"REQUIRED_{param_name.upper()}"
                else:
                    example_params[param_name] = f"optional_{param_name}"
            
            if example_params:
                example["arguments"]["parameters"] = example_params
        
        return example