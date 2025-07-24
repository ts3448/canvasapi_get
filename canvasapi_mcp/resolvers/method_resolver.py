"""
Dynamic method resolution for Canvas API objects.

This module provides functionality to discover and resolve Canvas API methods
dynamically, enabling the MCP server to call any Canvas method without
hardcoding specific method lists.
"""

import inspect
from canvasapi_get.canvas import Canvas
from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.exceptions import CanvasException
from ..validation import ValidationError, validator


class MethodResolutionError(Exception):
    """Raised when method resolution fails."""

    pass


class MethodResolver:
    """
    Resolves Canvas API methods dynamically for MCP tool invocation.

    This class provides the core functionality to:
    1. Discover available methods on Canvas objects
    2. Resolve Canvas objects by type and ID
    3. Validate and execute method calls with parameters
    4. Execute methods through the existing Canvas infrastructure
    """

    def __init__(self, canvas: Canvas):
        """
        Initialize the method resolver with a Canvas instance.

        Args:
            canvas: Canvas API instance for method resolution
        """
        self.canvas = canvas
        self._method_cache = {}
        self._object_cache = {}

    def discover_methods(
        self, obj: Canvas | CanvasObject, method_prefix: str = ""
    ) -> list[dict]:
        """
        Discover all available GET methods on a Canvas object.

        Args:
            obj: Canvas or CanvasObject instance to inspect
            method_prefix: Optional prefix to filter methods

        Returns:
            List of method information dictionaries
        """
        methods = []

        for attr_name in dir(obj):
            if attr_name.startswith("_"):
                continue

            if method_prefix and not attr_name.startswith(method_prefix):
                continue

            try:
                attr = getattr(obj, attr_name)
                if not callable(attr):
                    continue

                # Skip non-GET methods based on naming conventions
                if any(
                    attr_name.startswith(prefix)
                    for prefix in ["create_", "update_", "delete_", "edit_"]
                ):
                    continue

                # Get method signature and docstring
                try:
                    sig = inspect.signature(attr)
                    doc = inspect.getdoc(attr) or ""

                    method_info = {
                        "name": attr_name,
                        "signature": str(sig),
                        "docstring": doc,
                        "parameters": {},
                        "object_type": type(obj).__name__,
                    }

                    # Extract parameter information
                    for param_name, param in sig.parameters.items():
                        if param_name in ["self", "args", "kwargs"]:
                            continue

                        param_info = {
                            "name": param_name,
                            "required": param.default == inspect.Parameter.empty,
                            "default": (
                                param.default
                                if param.default != inspect.Parameter.empty
                                else None
                            ),
                            "annotation": (
                                param.annotation
                                if param.annotation != inspect.Parameter.empty
                                else None
                            ),
                        }

                        method_info["parameters"][param_name] = param_info

                    methods.append(method_info)

                except (ValueError, TypeError) as e:
                    # Skip methods we can't inspect
                    continue

            except (AttributeError, TypeError):
                continue

        return methods

    def resolve_canvas_object(
        self, object_type: str, object_id: int | str, **kwargs
    ) -> CanvasObject:
        """
        Resolve a Canvas object by type and ID using dynamic method discovery.

        Args:
            object_type: Type of Canvas object (e.g., 'course', 'user')
            object_id: Canvas object ID
            **kwargs: Additional parameters for object resolution

        Returns:
            Resolved Canvas object instance

        Raises:
            MethodResolutionError: If object resolution fails
        """
        cache_key = f"{object_type}:{object_id}"

        # Check cache first
        if cache_key in self._object_cache:
            return self._object_cache[cache_key]

        try:
            # Use dynamic method resolution instead of hardcoded mappings
            # Try to find a get_* method on Canvas that matches the object type
            method_name = f"get_{object_type.lower()}"

            if not hasattr(self.canvas, method_name):
                raise MethodResolutionError(
                    f"No method found for object type '{object_type}'. "
                    f"Expected Canvas.{method_name}() method. "
                    f"Use discover_canvas_methods tool to see available methods."
                )

            # Get the method and call it
            method = getattr(self.canvas, method_name)
            canvas_obj = method(object_id, **kwargs)

            # Cache the resolved object
            self._object_cache[cache_key] = canvas_obj

            return canvas_obj

        except Exception as e:
            raise MethodResolutionError(
                f"Failed to resolve {object_type} with ID {object_id}: {str(e)}. "
                f"Use discover_canvas_methods tool to explore available object types."
            )

    def resolve_method_call(
        self,
        object_type: str,
        object_id: int | str,
        method_name: str,
        parameters: dict,
    ) -> callable:
        """
        Resolve and execute a Canvas API method call.

        Args:
            object_type: Type of Canvas object
            object_id: Canvas object ID
            method_name: Name of method to call
            parameters: Method parameters

        Returns:
            Method execution result

        Raises:
            MethodResolutionError: If method resolution or execution fails
        """
        try:
            # Handle Canvas class methods directly
            if object_type.lower() == "canvas":
                target_obj = self.canvas
            else:
                # Resolve the target object
                target_obj = self.resolve_canvas_object(object_type, object_id)

            # Check if method exists on the object
            if not hasattr(target_obj, method_name):
                raise MethodResolutionError(
                    f"Method {method_name} not found on {type(target_obj).__name__}"
                )

            method = getattr(target_obj, method_name)

            # Validate method is callable
            if not callable(method):
                raise MethodResolutionError(f"{method_name} is not a callable method")

            # Skip non-GET methods for safety
            if any(
                method_name.startswith(prefix)
                for prefix in ["create_", "update_", "delete_", "edit_"]
            ):
                raise MethodResolutionError(
                    f"Method {method_name} is not a GET operation and is not allowed"
                )

            # Validate parameters using the validation system
            validated_params = validator.validate_canvas_method_parameters(
                method_name, method, parameters
            )

            # Execute the method
            result = method(**validated_params)

            return result

        except ValidationError as e:
            raise MethodResolutionError(f"Parameter validation failed: {str(e)}")
        except CanvasException as e:
            raise MethodResolutionError(f"Canvas API error: {str(e)}")
        except Exception as e:
            raise MethodResolutionError(f"Method execution failed: {str(e)}")

    def get_method_info(self, object_type: str, method_name: str) -> dict:
        """
        Get detailed information about a specific method.

        Args:
            object_type: Type of Canvas object
            method_name: Name of the method

        Returns:
            Dictionary containing method information

        Raises:
            MethodResolutionError: If method info cannot be retrieved
        """
        try:
            # Create a temporary object instance to inspect
            if object_type.lower() == "canvas":
                obj = self.canvas
            else:
                # For other objects, we need a sample instance
                # This is a bit tricky since we need an ID, but we can inspect the class
                obj_class = getattr(
                    self.canvas, f"get_{object_type.lower()}"
                ).__self__.__class__
                # Get methods from the class instead
                methods = self.discover_methods(obj_class)
                for method_info in methods:
                    if method_info["name"] == method_name:
                        return method_info

                raise MethodResolutionError(
                    f"Method {method_name} not found on {object_type}"
                )

            methods = self.discover_methods(obj)
            for method_info in methods:
                if method_info["name"] == method_name:
                    return method_info

            raise MethodResolutionError(
                f"Method {method_name} not found on {object_type}"
            )

        except Exception as e:
            raise MethodResolutionError(f"Failed to get method info: {str(e)}")

    def clear_cache(self):
        """Clear the object resolution cache."""
        self._object_cache.clear()
        self._method_cache.clear()

    def get_available_object_types(self) -> list[str]:
        """
        Get list of available Canvas object types that can be resolved dynamically.

        Returns:
            List of object type names discovered from Canvas methods
        """
        object_types = ["canvas"]  # Canvas is always available

        # Discover object types by looking for get_* methods on Canvas
        for attr_name in dir(self.canvas):
            if attr_name.startswith("get_") and not attr_name.startswith("get__"):
                # Extract object type from method name (e.g., get_course -> course)
                object_type = attr_name[4:]  # Remove "get_" prefix
                if object_type and hasattr(self.canvas, attr_name):
                    method = getattr(self.canvas, attr_name)
                    if callable(method):
                        object_types.append(object_type)

        return sorted(list(set(object_types)))
