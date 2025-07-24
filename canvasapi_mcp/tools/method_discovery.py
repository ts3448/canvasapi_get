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
from ..utils.pandas_engine import PandasEngine


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
        self.pandas_engine = PandasEngine()
    
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
                        "default": False
                    }
                },
                "required": ["object_type"],
                "additionalProperties": False
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
                "pandas_operations": {
                    "available": True,
                    "operations_count": len(self.pandas_engine.get_available_operations()),
                    "note": "Use 'get_pandas_operations' for detailed pandas operation info"
                },
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
                "additionalProperties": False
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


class PandasOperationsTool:
    """
    Pandas operations information tool for MCP integration.
    
    This tool provides information about available pandas operations that can
    be applied server-side to Canvas data through the canvas_query tool.
    """
    
    def __init__(self, canvas: Canvas):
        """
        Initialize the pandas operations tool.
        
        Args:
            canvas: Canvas API instance (for consistency with other tools)
        """
        self.canvas = canvas
        self.pandas_engine = PandasEngine()
    
    def get_tool_definition(self) -> Tool:
        """
        Get the MCP tool definition for pandas operations info.
        
        Returns:
            MCP Tool definition
        """
        return Tool(
            name="get_pandas_operations",
            description="""
            Get information about available pandas operations for server-side Canvas data processing.
            
            This tool provides documentation about pandas operations that can be applied
            to Canvas data through the canvas_query tool's pandas_operations parameter.
            
            Examples:
            - List all operations: {"list_all": true}
            - Get specific operation info: {"operation_name": "query"}
            - Get operation examples: {"include_examples": true}
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "operation_name": {
                        "type": "string",
                        "description": "Specific pandas operation to get info about"
                    },
                    "list_all": {
                        "type": "boolean",
                        "description": "List all available operations",
                        "default": False
                    },
                    "include_examples": {
                        "type": "boolean",
                        "description": "Include usage examples for operations",
                        "default": False
                    },
                    "category": {
                        "type": "string",
                        "description": "Filter by operation category",
                        "enum": ["filtering", "sorting", "aggregation", "cleaning", "statistical"]
                    }
                },
                "additionalProperties": False
            }
        )
    
    async def execute(self, arguments: dict) -> list[TextContent]:
        """
        Execute pandas operations info retrieval.
        
        Args:
            arguments: Tool arguments from MCP request
            
        Returns:
            List of TextContent responses
        """
        try:
            operation_name = arguments.get("operation_name")
            list_all = arguments.get("list_all", False)
            include_examples = arguments.get("include_examples", False)
            category = arguments.get("category")
            
            if operation_name:
                # Get specific operation info
                all_operations = self.pandas_engine.get_available_operations()
                if operation_name not in all_operations:
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "operation_not_found",
                            "message": f"Operation '{operation_name}' not found",
                            "available_operations": list(all_operations.keys())
                        }, indent=2)
                    )]
                
                result = {
                    "success": True,
                    "operation_name": operation_name,
                    "operation_info": all_operations[operation_name],
                    "usage_example": self._generate_pandas_usage_example(operation_name, all_operations[operation_name])
                }
            
            elif list_all:
                # List all operations
                all_operations = self.pandas_engine.get_available_operations()
                
                # Filter by category if specified
                if category:
                    filtered_ops = self._filter_operations_by_category(all_operations, category)
                else:
                    filtered_ops = all_operations
                
                result = {
                    "success": True,
                    "total_operations": len(all_operations),
                    "displayed_operations": len(filtered_ops),
                    "category_filter": category or "none",
                    "operations": filtered_ops if include_examples else list(filtered_ops.keys()),
                    "operation_categories": self._get_operation_categories()
                }
                
                if include_examples:
                    result["example_sequences"] = self.pandas_engine.get_operation_examples()
            
            else:
                # Default: overview with categories
                all_operations = self.pandas_engine.get_available_operations()
                categories = self._get_operation_categories()
                
                result = {
                    "success": True,
                    "overview": "Pandas operations for server-side Canvas data processing",
                    "total_operations": len(all_operations),
                    "operation_categories": categories,
                    "example_sequences": self.pandas_engine.get_operation_examples() if include_examples else {},
                    "usage_info": {
                        "how_to_use": "Add 'pandas_operations' parameter to canvas_query tool",
                        "operations_format": "List of operation dictionaries with 'operation' key",
                        "example": [
                            {"operation": "query", "expr": "status == 'active'"},
                            {"operation": "sort_values", "by": "created_at", "ascending": False},
                            {"operation": "head", "n": 50}
                        ]
                    }
                }
            
            return [TextContent(
                type="text",
                text=json.dumps(result, indent=2, default=str)
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "pandas_operations_error",
                    "message": str(e),
                    "type": type(e).__name__
                }, indent=2)
            )]
    
    def _filter_operations_by_category(self, operations: dict, category: str) -> dict:
        """Filter operations by category."""
        category_mapping = {
            "filtering": ["query", "head", "tail", "sample", "dropna"],
            "sorting": ["sort_values", "sort_index"],
            "aggregation": ["groupby", "agg", "describe", "value_counts"],
            "cleaning": ["drop_duplicates", "fillna", "reset_index", "set_index"],
            "statistical": ["describe", "value_counts"]
        }
        
        if category not in category_mapping:
            return operations
        
        category_ops = category_mapping[category]
        return {k: v for k, v in operations.items() if k in category_ops}
    
    def _get_operation_categories(self) -> dict:
        """Get operation categories with descriptions."""
        return {
            "filtering": {
                "description": "Filter and select data",
                "operations": ["query", "head", "tail", "sample", "dropna"]
            },
            "sorting": {
                "description": "Sort data by columns or index",
                "operations": ["sort_values", "sort_index"]
            },
            "aggregation": {
                "description": "Group and aggregate data",
                "operations": ["groupby", "agg", "describe", "value_counts"]
            },
            "cleaning": {
                "description": "Clean and transform data structure",
                "operations": ["drop_duplicates", "fillna", "reset_index", "set_index"]
            },
            "statistical": {
                "description": "Statistical analysis and summaries",
                "operations": ["describe", "value_counts"]
            }
        }
    
    def _generate_pandas_usage_example(self, operation_name: str, operation_info: dict) -> dict:
        """Generate usage example for a pandas operation."""
        base_example = {
            "tool": "canvas_query",
            "arguments": {
                "object_type": "course",
                "object_id": "YOUR_COURSE_ID",
                "method": "get_enrollments",
                "pandas_operations": [
                    json.loads(operation_info["example"])
                ],
                "output_format": "dataframe"
            }
        }
        
        return {
            "single_operation": base_example,
            "in_sequence": {
                "description": f"Using {operation_name} as part of a sequence",
                "example": {
                    "tool": "canvas_query",
                    "arguments": {
                        "object_type": "course",
                        "object_id": "YOUR_COURSE_ID", 
                        "method": "get_enrollments",
                        "pandas_operations": [
                            {"operation": "dropna", "subset": ["email"]},
                            json.loads(operation_info["example"]),
                            {"operation": "head", "n": 100}
                        ],
                        "output_format": "csv"
                    }
                }
            }
        }