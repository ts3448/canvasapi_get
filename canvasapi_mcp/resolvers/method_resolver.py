"""
Dynamic method resolution for Canvas API objects.

This module provides functionality to discover and resolve Canvas API methods
dynamically, enabling the MCP server to call any Canvas method without
hardcoding specific method lists.
"""

import inspect
from typing import Any, Dict, List, Optional, Tuple, Type, Union, get_type_hints
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
    2. Resolve method calls with parameter validation  
    3. Handle object chaining and ID resolution
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
    
    def discover_methods(self, obj: Union[Canvas, CanvasObject], method_prefix: str = "") -> List[Dict[str, Any]]:
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
            if attr_name.startswith('_'):
                continue
                
            if method_prefix and not attr_name.startswith(method_prefix):
                continue
                
            try:
                attr = getattr(obj, attr_name)
                if not callable(attr):
                    continue
                    
                # Skip non-GET methods based on naming conventions
                if any(attr_name.startswith(prefix) for prefix in ['create_', 'update_', 'delete_', 'edit_']):
                    continue
                    
                # Get method signature and docstring
                try:
                    sig = inspect.signature(attr)
                    doc = inspect.getdoc(attr) or ""
                    
                    # Get type hints if available
                    type_hints = {}
                    try:
                        type_hints = get_type_hints(attr)
                    except (NameError, AttributeError, TypeError):
                        pass
                    
                    method_info = {
                        'name': attr_name,
                        'signature': str(sig),
                        'docstring': doc,
                        'parameters': {},
                        'type_hints': type_hints,
                        'object_type': type(obj).__name__
                    }
                    
                    # Extract parameter information
                    for param_name, param in sig.parameters.items():
                        if param_name in ['self', 'args', 'kwargs']:
                            continue
                            
                        param_info = {
                            'name': param_name,
                            'required': param.default == inspect.Parameter.empty,
                            'default': param.default if param.default != inspect.Parameter.empty else None,
                            'annotation': param.annotation if param.annotation != inspect.Parameter.empty else None
                        }
                        
                        # Add type hint information if available
                        if param_name in type_hints:
                            param_info['type_hint'] = type_hints[param_name]
                            
                        method_info['parameters'][param_name] = param_info
                    
                    methods.append(method_info)
                    
                except (ValueError, TypeError) as e:
                    # Skip methods we can't inspect
                    continue
                    
            except (AttributeError, TypeError):
                continue
        
        return methods
    
    def resolve_canvas_object(self, object_type: str, object_id: Union[int, str], **kwargs) -> CanvasObject:
        """
        Resolve a Canvas object by type and ID.
        
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
            # Map object types to Canvas methods
            object_resolvers = {
                'account': lambda id: self.canvas.get_account(id),
                'course': lambda id: self.canvas.get_course(id),
                'user': lambda id: self.canvas.get_user(id),
                'group': lambda id: self.canvas.get_group(id),
                'section': lambda id: self.canvas.get_section(id),
                'enrollment_term': lambda id: self.canvas.get_enrollment_term(id),
                'external_tool': lambda id: self.canvas.get_external_tool(id),
            }
            
            resolver = object_resolvers.get(object_type.lower())
            if not resolver:
                raise MethodResolutionError(f"Unknown object type: {object_type}")
            
            # Resolve the object
            canvas_obj = resolver(object_id)
            
            # Cache the resolved object
            self._object_cache[cache_key] = canvas_obj
            
            return canvas_obj
            
        except Exception as e:
            raise MethodResolutionError(f"Failed to resolve {object_type} with ID {object_id}: {str(e)}")
    
    def resolve_nested_object(self, parent_obj: CanvasObject, child_type: str, child_id: Union[int, str]) -> CanvasObject:
        """
        Resolve a nested Canvas object from a parent object.
        
        Args:
            parent_obj: Parent Canvas object
            child_type: Type of child object to resolve
            child_id: Child object ID
            
        Returns:
            Resolved child Canvas object
            
        Raises:
            MethodResolutionError: If nested object resolution fails
        """
        try:
            # Common nested object patterns
            nested_resolvers = {
                'assignment': 'get_assignment',
                'discussion_topic': 'get_discussion_topic', 
                'quiz': 'get_quiz',
                'module': 'get_module',
                'page': 'get_page',
                'file': 'get_file',
                'folder': 'get_folder',
                'user': 'get_user',
                'enrollment': 'get_enrollment',
                'section': 'get_section',
                'group': 'get_group',
                'calendar_event': 'get_calendar_event',
                'submission': 'get_submission',
                'rubric': 'get_rubric',
                'external_tool': 'get_external_tool'
            }
            
            method_name = nested_resolvers.get(child_type.lower())
            if not method_name:
                raise MethodResolutionError(f"Unknown nested object type: {child_type}")
            
            if not hasattr(parent_obj, method_name):
                raise MethodResolutionError(f"Object {type(parent_obj).__name__} does not have method {method_name}")
            
            method = getattr(parent_obj, method_name)
            return method(child_id)
            
        except Exception as e:
            raise MethodResolutionError(f"Failed to resolve nested {child_type} with ID {child_id}: {str(e)}")
    
    def resolve_method_call(
        self, 
        object_type: str, 
        object_id: Union[int, str], 
        method_name: str, 
        parameters: Dict[str, Any]
    ) -> Any:
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
            if object_type.lower() == 'canvas':
                target_obj = self.canvas
            else:
                # Resolve the target object
                target_obj = self.resolve_canvas_object(object_type, object_id)
            
            # Check if method exists on the object
            if not hasattr(target_obj, method_name):
                raise MethodResolutionError(f"Method {method_name} not found on {type(target_obj).__name__}")
            
            method = getattr(target_obj, method_name)
            
            # Validate method is callable
            if not callable(method):
                raise MethodResolutionError(f"{method_name} is not a callable method")
            
            # Skip non-GET methods for safety
            if any(method_name.startswith(prefix) for prefix in ['create_', 'update_', 'delete_', 'edit_']):
                raise MethodResolutionError(f"Method {method_name} is not a GET operation and is not allowed")
            
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
    
    def resolve_chained_method_call(
        self,
        object_chain: List[Dict[str, Any]],
        method_name: str,
        parameters: Dict[str, Any]
    ) -> Any:
        """
        Resolve and execute a chained method call across multiple objects.
        
        Args:
            object_chain: List of object resolution steps
            method_name: Final method to call
            parameters: Method parameters
            
        Returns:
            Method execution result
            
        Raises:
            MethodResolutionError: If chain resolution fails
        """
        try:
            current_obj = None
            
            # Walk through the object chain
            for i, step in enumerate(object_chain):
                if i == 0:
                    # First step - resolve from Canvas
                    current_obj = self.resolve_canvas_object(
                        step['object_type'], 
                        step['object_id']
                    )
                else:
                    # Subsequent steps - resolve from parent
                    current_obj = self.resolve_nested_object(
                        current_obj,
                        step['object_type'],
                        step['object_id'] 
                    )
            
            if current_obj is None:
                raise MethodResolutionError("Object chain resolution failed")
            
            # Execute the final method on the resolved object
            if not hasattr(current_obj, method_name):
                raise MethodResolutionError(f"Method {method_name} not found on {type(current_obj).__name__}")
            
            method = getattr(current_obj, method_name)
            
            # Validate and execute
            validated_params = validator.validate_canvas_method_parameters(
                method_name, method, parameters
            )
            
            return method(**validated_params)
            
        except Exception as e:
            raise MethodResolutionError(f"Chained method call failed: {str(e)}")
    
    def get_method_info(self, object_type: str, method_name: str) -> Dict[str, Any]:
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
            if object_type.lower() == 'canvas':
                obj = self.canvas
            else:
                # For other objects, we need a sample instance
                # This is a bit tricky since we need an ID, but we can inspect the class
                obj_class = getattr(self.canvas, f"get_{object_type.lower()}").__self__.__class__
                # Get methods from the class instead
                methods = self.discover_methods(obj_class)
                for method_info in methods:
                    if method_info['name'] == method_name:
                        return method_info
                
                raise MethodResolutionError(f"Method {method_name} not found on {object_type}")
            
            methods = self.discover_methods(obj)
            for method_info in methods:
                if method_info['name'] == method_name:
                    return method_info
            
            raise MethodResolutionError(f"Method {method_name} not found on {object_type}")
            
        except Exception as e:
            raise MethodResolutionError(f"Failed to get method info: {str(e)}")
    
    def clear_cache(self):
        """Clear the object resolution cache."""
        self._object_cache.clear()
        self._method_cache.clear()
    
    def get_available_object_types(self) -> List[str]:
        """
        Get list of available Canvas object types that can be resolved.
        
        Returns:
            List of object type names
        """
        return [
            'canvas', 'account', 'course', 'user', 'group', 'section',
            'enrollment_term', 'external_tool', 'assignment', 'discussion_topic',
            'quiz', 'module', 'page', 'file', 'folder', 'enrollment',
            'calendar_event', 'submission', 'rubric'
        ]