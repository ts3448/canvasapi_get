"""
Parameter validation module for MCP server integration.

This module provides comprehensive validation functionality for converting MCP tool
parameters to Canvas API method parameters, handling ID formats, type validation,
and kwargs processing.
"""

import inspect
from collections.abc import Sequence
from datetime import datetime, date
from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.exceptions import RequiredFieldMissing
from canvasapi_get.util import obj_or_id, combine_kwargs, normalize_bool, is_multivalued


class ValidationError(Exception):
    """Raised when parameter validation fails."""

    def __init__(
        self, parameter_name: str, message: str, expected_type: str | None = None
    ):
        self.parameter_name = parameter_name
        self.expected_type = expected_type
        super().__init__(f"Parameter '{parameter_name}': {message}")


class ScopingRequiredError(ValidationError):
    """Raised when a method requires scoping parameters to follow Canvas data hierarchy."""
    
    def __init__(self, method_name: str, required_params: list[str]):
        self.method_name = method_name
        self.required_params = required_params
        super().__init__(
            "scoping_parameters", 
            f"Method {method_name} requires one of: {', '.join(required_params)} "
            f"to follow proper Canvas data hierarchy and prevent large data dumps. "
            f"This teaches efficient Canvas administrative workflows."
        )


class ParameterValidator:
    """
    Validates and converts parameters for Canvas API method calls.

    Handles conversion between MCP tool parameters and Canvas method parameters,
    including ID format validation, type checking, and kwargs processing.
    """

    # Methods that require scoping parameters to follow Canvas data hierarchy
    # Structure: "method_name": {"any": [...]} or {"all": [...]}
    METHODS_REQUIRING_SCOPING = {
        # Course queries - require academic term thinking (TESTED: 14K+ → hundreds)
        "get_courses": {"any": ["enrollment_term_id"]},
        
        # User queries - require BOTH term and role scoping (enrollment_type alone = 50K+ users)
        "get_users": {"all": ["enrollment_term_id", "enrollment_type"]},
        
        # Group queries - account-level groups can be massive, scope by term
        "get_groups": {"any": ["enrollment_term_id"]},
        
        # Section queries - account-level sections can be massive, scope by term  
        "get_sections": {"any": ["enrollment_term_id"]},
        
        # Enrollment queries - require term and role scoping to prevent massive dumps
        # Note: get_enrollments exists in Canvas API but not yet in Python wrapper
        "get_enrollments": {"all": ["enrollment_term_id", "enrollment_type"]},
        
        # External tools - may be many across entire account
        "get_external_tools": {"any": ["enrollment_term_id"]},
        
        # Additional endpoints identified from Canvas API documentation analysis
    }

    # Canvas object types mapping for ID validation
    CANVAS_OBJECT_TYPES = {
        "account": None,  # Will be populated dynamically to avoid circular imports
        "assignment": None,
        "course": None,
        "user": None,
        "group": None,
        "section": None,
        "enrollment": None,
        "discussion_topic": None,
        "module": None,
        "quiz": None,
        "submission": None,
        "file": None,
        "folder": None,
        "page": None,
        "calendar_event": None,
        "announcement": None,
        "rubric": None,
        "grading_standard": None,
        "outcome": None,
        "external_tool": None,
    }

    # Common Canvas API parameter types
    PARAMETER_TYPES = {
        "string": str,
        "integer": int,
        "float": float,
        "boolean": bool,
        "datetime": (str, datetime, date),
        "array": (list, tuple),
        "object": dict,
    }

    def __init__(self):
        """Initialize the parameter validator."""
        self._populate_canvas_types()

    def _populate_canvas_types(self):
        """Dynamically populate Canvas object types to avoid circular imports."""
        try:
            from canvasapi_get.account import Account
            from canvasapi_get.assignment import Assignment
            from canvasapi_get.course import Course
            from canvasapi_get.user import User
            from canvasapi_get.group import Group
            from canvasapi_get.section import Section
            from canvasapi_get.enrollment import Enrollment
            from canvasapi_get.discussion_topic import DiscussionTopic
            from canvasapi_get.module import Module
            from canvasapi_get.quiz import Quiz
            from canvasapi_get.submission import Submission
            from canvasapi_get.file import File
            from canvasapi_get.folder import Folder
            from canvasapi_get.page import Page
            from canvasapi_get.calendar_event import CalendarEvent
            from canvasapi_get.rubric import Rubric
            from canvasapi_get.grading_standard import GradingStandard
            from canvasapi_get.outcome import Outcome
            from canvasapi_get.external_tool import ExternalTool

            self.CANVAS_OBJECT_TYPES.update(
                {
                    "account": Account,
                    "assignment": Assignment,
                    "course": Course,
                    "user": User,
                    "group": Group,
                    "section": Section,
                    "enrollment": Enrollment,
                    "discussion_topic": DiscussionTopic,
                    "module": Module,
                    "quiz": Quiz,
                    "submission": Submission,
                    "file": File,
                    "folder": Folder,
                    "page": Page,
                    "calendar_event": CalendarEvent,
                    "rubric": Rubric,
                    "grading_standard": GradingStandard,
                    "outcome": Outcome,
                    "external_tool": ExternalTool,
                }
            )
        except ImportError as e:
            # Some modules might not be available, continue with what we have
            pass

    def validate_id_parameter(
        self,
        parameter,
        param_name: str,
        object_types: str | list[str] | tuple[type, ...],
    ) -> int | str:
        """
        Validate and convert Canvas object ID parameter.

        Args:
            parameter: The parameter value (object, int, or string)
            param_name: Name of the parameter for error reporting
            object_types: Expected Canvas object type(s)

        Returns:
            Valid Canvas ID (int or string like "self")

        Raises:
            ValidationError: If parameter is invalid
        """
        # Handle string object type names
        if isinstance(object_types, str):
            object_types = [object_types]

        # Convert string names to actual types
        if isinstance(object_types, (list, tuple)) and object_types:
            if isinstance(object_types[0], str):
                type_objs = []
                for type_name in object_types:
                    canvas_type = self.CANVAS_OBJECT_TYPES.get(type_name.lower())
                    if canvas_type:
                        type_objs.append(canvas_type)
                object_types = tuple(type_objs) if type_objs else object_types

        try:
            return obj_or_id(parameter, param_name, object_types)
        except (TypeError, ValueError) as e:
            raise ValidationError(param_name, str(e))

    def validate_parameter_type(
        self, value, param_name: str, expected_type: str | type | list[str | type]
    ):
        """
        Validate parameter type and convert if necessary.

        Args:
            value: Parameter value to validate
            param_name: Parameter name for error reporting
            expected_type: Expected type(s) - can be string name or type object

        Returns:
            Validated/converted parameter value

        Raises:
            ValidationError: If type validation fails
        """
        if value is None:
            return None

        # Handle list of acceptable types
        if isinstance(expected_type, Sequence) and not isinstance(expected_type, str):
            for type_option in expected_type:
                try:
                    return self.validate_parameter_type(value, param_name, type_option)
                except ValidationError:
                    continue

            type_names = [str(t) for t in expected_type]
            raise ValidationError(
                param_name,
                f"must be one of types: {', '.join(type_names)}, got {type(value).__name__}",
            )

        # Handle string type names
        if isinstance(expected_type, str):
            expected_type = self.PARAMETER_TYPES.get(
                expected_type.lower(), expected_type
            )

        # Special handling for different types
        if expected_type == bool:
            try:
                return normalize_bool(value, param_name)
            except ValueError as e:
                raise ValidationError(param_name, str(e))

        elif expected_type == int:
            try:
                return int(value)
            except (ValueError, TypeError):
                raise ValidationError(
                    param_name, f"must be an integer, got {type(value).__name__}"
                )

        elif expected_type == float:
            try:
                return float(value)
            except (ValueError, TypeError):
                raise ValidationError(
                    param_name, f"must be a float, got {type(value).__name__}"
                )

        elif expected_type == str:
            return str(value)

        elif expected_type in ((str, datetime, date), (datetime, date)):
            # Handle datetime/date strings
            if isinstance(value, str):
                return value  # Canvas API accepts ISO 8601 strings
            elif isinstance(value, (datetime, date)):
                return value.isoformat()
            else:
                raise ValidationError(
                    param_name,
                    f"must be a date/datetime or string, got {type(value).__name__}",
                )

        elif expected_type in ((list, tuple), list, tuple):
            if not is_multivalued(value):
                raise ValidationError(
                    param_name, f"must be a list or array, got {type(value).__name__}"
                )
            return list(value) if not isinstance(value, list) else value

        elif expected_type == dict:
            if not isinstance(value, dict):
                raise ValidationError(
                    param_name, f"must be an object/dict, got {type(value).__name__}"
                )
            return value

        # Check if value is instance of expected type
        elif isinstance(expected_type, type):
            if not isinstance(value, expected_type):
                raise ValidationError(
                    param_name,
                    f"must be of type {expected_type.__name__}, got {type(value).__name__}",
                )
            return value

        # Handle tuple of types (union type)
        elif isinstance(expected_type, tuple):
            if not isinstance(value, expected_type):
                type_names = [t.__name__ for t in expected_type]
                raise ValidationError(
                    param_name,
                    f"must be one of types: {', '.join(type_names)}, got {type(value).__name__}",
                )
            return value

        return value

    def validate_required_parameters(
        self, parameters: dict, required_params: list[str]
    ):
        """
        Validate that all required parameters are present and not None.

        Args:
            parameters: Dictionary of provided parameters
            required_params: List of required parameter names

        Raises:
            RequiredFieldMissing: If any required parameter is missing or None
        """
        missing_params = []

        for param_name in required_params:
            if param_name not in parameters or parameters[param_name] is None:
                missing_params.append(param_name)

        if missing_params:
            raise RequiredFieldMissing(
                f"Required parameter(s) missing: {', '.join(missing_params)}"
            )

    def process_kwargs(self, kwargs: dict) -> list[tuple]:
        """
        Process kwargs dictionary for Canvas API calls using combine_kwargs utility.

        Args:
            kwargs: Dictionary of keyword arguments

        Returns:
            List of (key, value) tuples formatted for Canvas API
        """
        return combine_kwargs(**kwargs)

    def convert_canvas_object_to_dict(self, obj: CanvasObject) -> dict:
        """
        Convert Canvas object to dictionary representation for MCP responses.

        Args:
            obj: Canvas object instance

        Returns:
            Dictionary representation of the object
        """
        if not isinstance(obj, CanvasObject):
            raise ValidationError(
                "obj", f"must be a CanvasObject, got {type(obj).__name__}"
            )

        # Get all attributes except private ones and the requester
        result = {}
        for attr_name, attr_value in obj.__dict__.items():
            if not attr_name.startswith("_") and attr_name != "attributes":
                # Handle nested Canvas objects
                if isinstance(attr_value, CanvasObject):
                    result[attr_name] = self.convert_canvas_object_to_dict(attr_value)
                elif isinstance(attr_value, list):
                    result[attr_name] = [
                        (
                            self.convert_canvas_object_to_dict(item)
                            if isinstance(item, CanvasObject)
                            else item
                        )
                        for item in attr_value
                    ]
                else:
                    result[attr_name] = attr_value

        return result

    def extract_canvas_ids(self, obj: CanvasObject) -> dict[str, int | str]:
        """
        Extract all available ID formats from a Canvas object.

        Args:
            obj: Canvas object instance

        Returns:
            Dictionary containing available ID formats (id, sis_id, integration_id, etc.)
        """
        if not isinstance(obj, CanvasObject):
            raise ValidationError(
                "obj", f"must be a CanvasObject, got {type(obj).__name__}"
            )

        id_fields = {}

        # Common ID field patterns
        id_patterns = [
            "id",
            "sis_user_id",
            "sis_course_id",
            "sis_account_id",
            "sis_section_id",
            "integration_id",
            "lti_user_id",
            "uuid",
            "course_code",
            "account_id",
            "user_id",
            "group_id",
            "section_id",
            "enrollment_id",
        ]

        for pattern in id_patterns:
            if hasattr(obj, pattern):
                value = getattr(obj, pattern)
                if value is not None:
                    id_fields[pattern] = value

        return id_fields

    def validate_canvas_method_parameters(
        self, method_name: str, method_obj: callable, parameters: dict
    ) -> dict:
        """
        Validate parameters for a specific Canvas method call.

        Args:
            method_name: Name of the Canvas method
            method_obj: The actual method object for inspection
            parameters: Dictionary of parameters to validate

        Returns:
            Dictionary of validated parameters

        Raises:
            ValidationError: If parameter validation fails
        """
        validated = {}

        try:
            # Get method signature
            sig = inspect.signature(method_obj)

            # Get type hints if available
            type_hints = {}
            try:
                type_hints = getattr(method_obj, "__annotations__", {})
            except (NameError, AttributeError):
                # Type hints might not be available or use forward references
                pass

            # Validate each parameter
            for param_name, param_value in parameters.items():
                if param_name in sig.parameters:
                    param_info = sig.parameters[param_name]

                    # Check if parameter has type hint
                    if param_name in type_hints:
                        expected_type = type_hints[param_name]
                        validated[param_name] = self.validate_parameter_type(
                            param_value, param_name, expected_type
                        )
                    else:
                        # No type hint available, just pass through
                        validated[param_name] = param_value
                else:
                    # Parameter not in method signature, might be for kwargs
                    validated[param_name] = param_value

            # Check for required parameters (those without defaults)
            required_params = []
            for param_name, param_info in sig.parameters.items():
                if (
                    param_info.default == inspect.Parameter.empty
                    and param_name not in ["self", "args", "kwargs"]
                    and param_info.kind != inspect.Parameter.VAR_KEYWORD
                ):
                    required_params.append(param_name)

            # Validate required parameters are present
            provided_params = set(parameters.keys())
            missing_required = [p for p in required_params if p not in provided_params]

            if missing_required:
                raise RequiredFieldMissing(
                    f"Required parameter(s) missing for {method_name}: {', '.join(missing_required)}"
                )

        except Exception as e:
            if isinstance(e, (ValidationError, RequiredFieldMissing)):
                raise
            # If inspection fails, just return validated parameters as-is
            validated = parameters

        return validated

    def validate_scoping_requirements(self, method_name: str, parameters: dict):
        """
        Validate that methods requiring scoping parameters follow Canvas data hierarchy.
        
        This enforces proper Canvas administrative workflows by requiring parameters
        that scope queries appropriately and teach users the natural Canvas data flow.
        
        Args:
            method_name: Name of the Canvas method
            parameters: Dictionary of provided parameters
            
        Raises:
            ScopingRequiredError: If method requires scoping parameters but none provided
        """
        if method_name in self.METHODS_REQUIRING_SCOPING:
            scoping_config = self.METHODS_REQUIRING_SCOPING[method_name]
            
            # Handle both old format (list) and new format (dict)
            if isinstance(scoping_config, list):
                # Legacy format - treat as "any"
                validation_type = "any"
                required_params = scoping_config
            else:
                # New format - extract type and params
                validation_type = list(scoping_config.keys())[0]  # "any" or "all"
                required_params = scoping_config[validation_type]
            
            # Skip validation if no scoping parameters are required (empty list)
            if not required_params:
                return
            
            # Check parameters based on validation type
            if validation_type == "any":
                # Check if any of the required scoping parameters are present and non-empty
                has_scoping_param = any(
                    param in parameters and parameters[param] not in (None, "", [])
                    for param in required_params
                )
            else:  # validation_type == "all"
                # Check if all of the required scoping parameters are present and non-empty
                has_scoping_param = all(
                    param in parameters and parameters[param] not in (None, "", [])
                    for param in required_params
                )
            
            if not has_scoping_param:
                raise ScopingRequiredError(method_name, required_params)

    def format_validation_error(self, error: Exception) -> dict[str, str]:
        """
        Format validation error for MCP response.

        Args:
            error: The validation error

        Returns:
            Dictionary containing error information
        """
        if isinstance(error, ScopingRequiredError):
            # Provide method-specific guidance based on Canvas hierarchy
            suggestions = {
                "get_courses": {
                    "workflow": "Get enrollment terms first, then query courses by term",
                    "example": '{"parameters": {"enrollment_term_id": 583}}',
                    "reasoning": "Account-wide course queries can return 14,000+ courses (tested)"
                },
                "get_users": {
                    "workflow": "Specify BOTH enrollment term and user role for account-wide queries",
                    "example": '{"parameters": {"enrollment_term_id": 583, "enrollment_type": "StudentEnrollment"}}',
                    "reasoning": "Account-wide user queries need both term and role scoping (enrollment_type alone can return 50,000+ users)"
                },
                "get_groups": {
                    "workflow": "Get enrollment terms first, then query groups by term",
                    "example": '{"parameters": {"enrollment_term_id": 583}}',
                    "reasoning": "Account-wide group queries can return thousands of groups across all courses"
                },
                "get_sections": {
                    "workflow": "Get enrollment terms first, then query sections by term", 
                    "example": '{"parameters": {"enrollment_term_id": 583}}',
                    "reasoning": "Account-wide section queries can return massive numbers of sections"
                },
                "get_enrollments": {
                    "workflow": "Specify both enrollment term and type for proper scoping",
                    "example": '{"parameters": {"enrollment_term_id": 583, "enrollment_type": "StudentEnrollment"}}',
                    "reasoning": "Enrollment queries can return millions of records without proper scoping"
                },
                "get_external_tools": {
                    "workflow": "Get enrollment terms first to scope external tools by active period",
                    "example": '{"parameters": {"enrollment_term_id": 583}}',
                    "reasoning": "Account-wide external tool queries can return many tools across entire institution"
                }
            }
            
            method_guidance = suggestions.get(error.method_name, {
                "workflow": f"Provide one of: {', '.join(error.required_params)}",
                "example": f'{{\"parameters\": {{\"{error.required_params[0]}\": \"appropriate_value\"}}}}',
                "reasoning": "This method requires scoping to prevent large data dumps"
            })
            
            return {
                "error": "scoping_required",
                "method": error.method_name,
                "message": str(error),
                "required_parameters": error.required_params,
                "workflow_guidance": method_guidance["workflow"],
                "example": method_guidance["example"],
                "reasoning": method_guidance["reasoning"],
                "canvas_hierarchy": "Account → Enrollment Term → Course/User → Content"
            }
        elif isinstance(error, ValidationError):
            return {
                "error": "validation_error",
                "parameter": error.parameter_name,
                "message": str(error),
                "expected_type": error.expected_type,
            }
        elif isinstance(error, RequiredFieldMissing):
            return {"error": "required_field_missing", "message": str(error)}
        else:
            return {"error": "unknown_validation_error", "message": str(error)}


# Global validator instance
validator = ParameterValidator()


def validate_id_parameter(
    parameter, param_name: str, object_types: str | list[str]
) -> int | str:
    """
    Convenience function for ID parameter validation.

    Args:
        parameter: The parameter value
        param_name: Parameter name
        object_types: Expected Canvas object type(s)

    Returns:
        Validated Canvas ID
    """
    return validator.validate_id_parameter(parameter, param_name, object_types)


def validate_parameter_type(value, param_name: str, expected_type: str | type):
    """
    Convenience function for parameter type validation.

    Args:
        value: Parameter value
        param_name: Parameter name
        expected_type: Expected type

    Returns:
        Validated parameter value
    """
    return validator.validate_parameter_type(value, param_name, expected_type)


def validate_required_parameters(parameters: dict, required_params: list[str]):
    """
    Convenience function for required parameter validation.

    Args:
        parameters: Dictionary of parameters
        required_params: List of required parameter names
    """
    return validator.validate_required_parameters(parameters, required_params)


def process_kwargs(kwargs: dict) -> list[tuple]:
    """
    Convenience function for kwargs processing.

    Args:
        kwargs: Dictionary of keyword arguments

    Returns:
        List of (key, value) tuples for Canvas API
    """
    return validator.process_kwargs(kwargs)


def convert_canvas_object_to_dict(obj: CanvasObject) -> dict:
    """
    Convenience function for Canvas object to dict conversion.

    Args:
        obj: Canvas object instance

    Returns:
        Dictionary representation
    """
    return validator.convert_canvas_object_to_dict(obj)
