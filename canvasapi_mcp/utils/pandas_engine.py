"""
Server-side pandas operations engine for Canvas data processing.

This module provides safe, allowlisted pandas operations that can be applied
to complete Canvas datasets on the server-side, returning only filtered results
to clients. This approach leverages the async pagination infrastructure to
retrieve full datasets, then applies sophisticated filtering and processing
without requiring client-side data transfer.
"""

import pandas as pd
from collections.abc import Sequence
import logging

logger = logging.getLogger(__name__)


class PandasOperationError(Exception):
    """Raised when pandas operation execution fails."""

    pass


class PandasEngine:
    """
    Safe pandas operations engine for server-side Canvas data processing.

    This engine provides a secure way to execute pandas operations on Canvas
    DataFrames using an allowlist of safe methods. Operations are applied
    sequentially to provide SQL-like filtering capabilities without exposing
    unsafe pandas functionality.
    """

    def __init__(self):
        """Initialize the pandas engine with allowlisted operations."""
        # Core data selection and filtering operations
        self.allowed_operations = {
            # Data filtering and selection
            "query": {
                "description": "Filter rows using boolean expressions",
                "required_params": ["expr"],
                "optional_params": ["engine", "parser"],
                "example": '{"operation": "query", "expr": "enrollment_state == \'active\'"}',
            },
            "head": {
                "description": "Return first n rows",
                "required_params": [],
                "optional_params": ["n"],
                "example": '{"operation": "head", "n": 10}',
            },
            "tail": {
                "description": "Return last n rows",
                "required_params": [],
                "optional_params": ["n"],
                "example": '{"operation": "tail", "n": 10}',
            },
            "sample": {
                "description": "Return random sample of rows",
                "required_params": [],
                "optional_params": ["n", "frac", "random_state"],
                "example": '{"operation": "sample", "n": 100, "random_state": 42}',
            },
            # Sorting operations
            "sort_values": {
                "description": "Sort by one or more columns",
                "required_params": ["by"],
                "optional_params": ["ascending", "na_position"],
                "example": '{"operation": "sort_values", "by": "created_at", "ascending": false}',
            },
            "sort_index": {
                "description": "Sort by index values",
                "required_params": [],
                "optional_params": ["ascending", "na_position"],
                "example": '{"operation": "sort_index", "ascending": true}',
            },
            # Data cleaning operations
            "drop_duplicates": {
                "description": "Remove duplicate rows",
                "required_params": [],
                "optional_params": ["subset", "keep"],
                "example": '{"operation": "drop_duplicates", "subset": ["user_id"], "keep": "first"}',
            },
            "dropna": {
                "description": "Remove rows with missing values",
                "required_params": [],
                "optional_params": ["axis", "how", "thresh", "subset"],
                "example": '{"operation": "dropna", "subset": ["email"], "how": "any"}',
            },
            "fillna": {
                "description": "Fill missing values",
                "required_params": ["value"],
                "optional_params": ["method", "axis", "limit"],
                "example": '{"operation": "fillna", "value": "Unknown"}',
            },
            # Aggregation operations
            "groupby": {
                "description": "Group by one or more columns for aggregation",
                "required_params": ["by"],
                "optional_params": ["as_index", "sort", "dropna"],
                "example": '{"operation": "groupby", "by": "course_id", "as_index": false}',
            },
            "agg": {
                "description": "Apply aggregation functions (use after groupby)",
                "required_params": ["func"],
                "optional_params": [],
                "example": '{"operation": "agg", "func": {"enrollment_count": "count", "avg_score": "mean"}}',
            },
            # Statistical operations
            "describe": {
                "description": "Generate descriptive statistics",
                "required_params": [],
                "optional_params": ["percentiles", "include", "exclude"],
                "example": '{"operation": "describe"}',
            },
            "value_counts": {
                "description": "Count unique values in a column",
                "required_params": [],
                "optional_params": ["normalize", "sort", "ascending", "dropna"],
                "example": '{"operation": "value_counts", "normalize": true}',
            },
            # Index operations
            "reset_index": {
                "description": "Reset DataFrame index",
                "required_params": [],
                "optional_params": ["drop", "inplace"],
                "example": '{"operation": "reset_index", "drop": true}',
            },
            "set_index": {
                "description": "Set DataFrame index using column(s)",
                "required_params": ["keys"],
                "optional_params": ["drop", "append"],
                "example": '{"operation": "set_index", "keys": "user_id", "drop": true}',
            },
        }

        # Safe aggregation functions for groupby operations
        self.allowed_agg_functions = {
            "count",
            "sum",
            "mean",
            "median",
            "min",
            "max",
            "std",
            "var",
            "first",
            "last",
            "nunique",
            "size",
        }

    def get_available_operations(self) -> dict[str, dict]:
        """
        Get documentation for all available pandas operations.

        Returns:
            Dictionary mapping operation names to their documentation
        """
        return self.allowed_operations.copy()

    def validate_operation(self, operation: dict) -> dict:
        """
        Validate a pandas operation before execution.

        Args:
            operation: Dictionary containing operation details

        Returns:
            Validated operation dictionary

        Raises:
            PandasOperationError: If operation is invalid or unsafe
        """
        if not isinstance(operation, dict):
            raise PandasOperationError("Operation must be a dictionary")

        operation_name = operation.get("operation")
        if not operation_name:
            raise PandasOperationError("Operation must specify 'operation' field")

        if operation_name not in self.allowed_operations:
            available = ", ".join(sorted(self.allowed_operations.keys()))
            raise PandasOperationError(
                f"Operation '{operation_name}' is not allowed. "
                f"Available operations: {available}"
            )

        op_spec = self.allowed_operations[operation_name]

        # Check required parameters
        for param in op_spec["required_params"]:
            if param not in operation:
                raise PandasOperationError(
                    f"Operation '{operation_name}' requires parameter '{param}'"
                )

        # Validate aggregation functions for groupby operations
        if operation_name == "agg":
            func = operation.get("func")
            if isinstance(func, dict):
                for agg_func in func.values():
                    if agg_func not in self.allowed_agg_functions:
                        allowed_funcs = ", ".join(sorted(self.allowed_agg_functions))
                        raise PandasOperationError(
                            f"Aggregation function '{agg_func}' is not allowed. "
                            f"Available functions: {allowed_funcs}"
                        )
            elif isinstance(func, (str, list)):
                funcs = [func] if isinstance(func, str) else func
                for agg_func in funcs:
                    if agg_func not in self.allowed_agg_functions:
                        allowed_funcs = ", ".join(sorted(self.allowed_agg_functions))
                        raise PandasOperationError(
                            f"Aggregation function '{agg_func}' is not allowed. "
                            f"Available functions: {allowed_funcs}"
                        )

        return operation

    def apply_operations(
        self, dataframe: pd.DataFrame, operations: Sequence[dict]
    ) -> pd.DataFrame:
        """
        Apply a sequence of pandas operations to a DataFrame.

        Args:
            dataframe: Input DataFrame to process
            operations: List of operation dictionaries to apply sequentially

        Returns:
            Processed DataFrame after applying all operations

        Raises:
            PandasOperationError: If any operation fails
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise PandasOperationError("Input must be a pandas DataFrame")

        if not operations:
            return dataframe

        result = dataframe.copy()
        operation_results = []
        operation_name = "unknown"
        i = -1

        try:
            for i, operation in enumerate(operations):
                validated_op = self.validate_operation(operation)
                operation_name = validated_op["operation"]

                logger.info(
                    f"Applying operation {i+1}/{len(operations)}: {operation_name}"
                )

                # Special validation for groupby operations
                if operation_name == "groupby":
                    # Check if next operation is agg
                    if (
                        i + 1 >= len(operations)
                        or operations[i + 1].get("operation") != "agg"
                    ):
                        raise PandasOperationError(
                            "groupby operation must be followed by agg operation"
                        )

                # Apply the operation
                result = self._execute_operation(result, validated_op)

                # Track operation results for debugging
                operation_results.append(
                    {
                        "operation": operation_name,
                        "rows_before": (
                            len(dataframe)
                            if i == 0
                            else operation_results[i - 1].get("rows_after", 0)
                        ),
                        "rows_after": (
                            len(result)
                            if hasattr(result, "__len__") and hasattr(result, "columns")
                            else "N/A"
                        ),
                        "columns": (
                            len(result.columns) if hasattr(result, "columns") else "N/A"
                        ),
                        "result_type": type(result).__name__,
                    }
                )

            logger.info(f"Successfully applied {len(operations)} operations")
            return result

        except Exception as e:
            if i >= 0:
                operation_context = f"operation {i+1} ({operation_name})"
            else:
                operation_context = "validation"
            raise PandasOperationError(
                f"Failed to apply pandas operations at {operation_context}: {str(e)}"
            )

    def _execute_operation(
        self, dataframe: pd.DataFrame, operation: dict
    ) -> pd.DataFrame:
        """
        Execute a single validated pandas operation.

        Args:
            dataframe: DataFrame to operate on
            operation: Validated operation dictionary

        Returns:
            DataFrame after applying the operation
        """
        operation_name = operation["operation"]

        # Remove 'operation' key to pass remaining as kwargs
        kwargs = {k: v for k, v in operation.items() if k != "operation"}

        try:
            if operation_name == "query":
                return dataframe.query(**kwargs)
            elif operation_name == "head":
                return dataframe.head(**kwargs)
            elif operation_name == "tail":
                return dataframe.tail(**kwargs)
            elif operation_name == "sample":
                return dataframe.sample(**kwargs)
            elif operation_name == "sort_values":
                return dataframe.sort_values(**kwargs)
            elif operation_name == "sort_index":
                return dataframe.sort_index(**kwargs)
            elif operation_name == "drop_duplicates":
                return dataframe.drop_duplicates(**kwargs)
            elif operation_name == "dropna":
                return dataframe.dropna(**kwargs)
            elif operation_name == "fillna":
                return dataframe.fillna(**kwargs)
            elif operation_name == "groupby":
                # For groupby, we return the grouped object for potential aggregation
                # This should only be used when followed by agg operation
                return dataframe.groupby(**kwargs)
            elif operation_name == "agg":
                # This should only be called on a grouped DataFrame
                if hasattr(dataframe, "agg") and hasattr(dataframe, "obj"):
                    # This is a GroupBy object
                    func = kwargs["func"]
                    if isinstance(func, dict):
                        # For named aggregations, we need to apply functions to specific columns
                        result = dataframe.agg(func)
                    else:
                        result = dataframe.agg(func)

                    # Reset index to ensure we return a clean DataFrame
                    if hasattr(result, "reset_index"):
                        result = result.reset_index()
                    return result
                else:
                    raise PandasOperationError(
                        "agg operation can only be used after groupby"
                    )
            elif operation_name == "describe":
                return dataframe.describe(**kwargs)
            elif operation_name == "value_counts":
                # value_counts returns a Series, convert to DataFrame
                if len(dataframe.columns) == 1:
                    col_name = dataframe.columns[0]
                    result = dataframe[col_name].value_counts(**kwargs)
                    return result.reset_index()
                else:
                    raise PandasOperationError(
                        "value_counts requires a single column DataFrame"
                    )
            elif operation_name == "reset_index":
                return dataframe.reset_index(**kwargs)
            elif operation_name == "set_index":
                return dataframe.set_index(**kwargs)
            else:
                raise PandasOperationError(f"Unknown operation: {operation_name}")

        except Exception as e:
            raise PandasOperationError(f"Operation {operation_name} failed: {str(e)}")

    def get_operation_examples(self) -> dict[str, list[dict]]:
        """
        Get example operation sequences for common use cases.

        Returns:
            Dictionary mapping use case names to operation sequences
        """
        return {
            "filter_and_sort": [
                {"operation": "query", "expr": "status == 'active'"},
                {"operation": "sort_values", "by": "created_at", "ascending": False},
                {"operation": "head", "n": 50},
            ],
            "group_and_aggregate": [
                {"operation": "dropna", "subset": ["course_id"]},
                {"operation": "groupby", "by": "course_id", "as_index": False},
                {
                    "operation": "agg",
                    "func": {"student_count": "count", "avg_score": "mean"},
                },
            ],
            "data_cleaning": [
                {
                    "operation": "drop_duplicates",
                    "subset": ["user_id"],
                    "keep": "first",
                },
                {"operation": "fillna", "value": "Unknown"},
                {"operation": "sort_values", "by": "name"},
            ],
            "statistical_summary": [
                {"operation": "describe"},
                {"operation": "reset_index"},
            ],
        }

    def estimate_memory_usage(self, dataframe: pd.DataFrame) -> dict[str, str | int]:
        """
        Estimate memory usage for DataFrame operations.

        Args:
            dataframe: DataFrame to analyze

        Returns:
            Dictionary with memory usage statistics
        """
        try:
            memory_usage = dataframe.memory_usage(deep=True).sum()

            return {
                "rows": len(dataframe),
                "columns": len(dataframe.columns),
                "memory_bytes": int(memory_usage),
                "memory_mb": round(memory_usage / (1024 * 1024), 2),
                "estimated_safe": memory_usage < 100 * 1024 * 1024,  # 100MB threshold
            }
        except Exception as e:
            logger.warning(f"Could not estimate memory usage: {e}")
            return {
                "rows": len(dataframe),
                "columns": len(dataframe.columns),
                "memory_bytes": 0,
                "memory_mb": 0.0,
                "estimated_safe": True,
            }
