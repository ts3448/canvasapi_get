"""
Universal Canvas object to DataFrame converter.

This module provides comprehensive functionality for converting Canvas API objects
and paginated lists to pandas DataFrames with intelligent schema mapping,
memory optimization, and data type normalization.
"""

import gc
import logging
from datetime import datetime, date
import pandas as pd
import numpy as np
from canvasapi_get.canvas_object import CanvasObject
from canvasapi_get.paginated_list import PaginatedList
from .attribute_discovery import AttributeDiscovery

logger = logging.getLogger(__name__)


class DataFrameConversionError(Exception):
    """Raised when DataFrame conversion fails."""
    pass


class DataFrameConverter:
    """
    Universal converter for Canvas objects to pandas DataFrames.
    
    Handles single objects, lists, and PaginatedList with memory optimization,
    schema discovery, and consistent data type conversion across all Canvas
    object types.
    """
    
    def __init__(self, batch_size: int = 1000, max_depth: int = 3, memory_limit_mb: int = 500):
        """
        Initialize the DataFrame converter.
        
        Args:
            batch_size: Number of objects to process in each batch
            max_depth: Maximum depth for nested object flattening
            memory_limit_mb: Memory limit in MB for batch processing
        """
        self.batch_size = batch_size
        self.max_depth = max_depth
        self.memory_limit_mb = memory_limit_mb
        self.attribute_discovery = AttributeDiscovery()
        
        # Schema cache for consistent column mapping
        self._schema_cache = {}
        self._type_cache = {}
    
    def convert_to_dataframe(
        self, 
        data: CanvasObject | list[CanvasObject] | PaginatedList,
        object_type: str | None = None,
        include_metadata: bool = False,
        flatten_nested: bool = True
    ) -> pd.DataFrame:
        """
        Convert Canvas data to pandas DataFrame.
        
        Args:
            data: Canvas object(s) to convert
            object_type: Optional object type hint for schema optimization
            include_metadata: Include conversion metadata in result
            flatten_nested: Whether to flatten nested Canvas objects
            
        Returns:
            pandas DataFrame with optimized data types
            
        Raises:
            DataFrameConversionError: If conversion fails
        """
        try:
            if isinstance(data, CanvasObject):
                return self._convert_single_object(data, object_type, flatten_nested)
            elif isinstance(data, PaginatedList):
                return self._convert_paginated_list(data, object_type, flatten_nested)
            elif isinstance(data, list):
                return self._convert_object_list(data, object_type, flatten_nested)
            else:
                raise DataFrameConversionError(f"Unsupported data type: {type(data)}")
                
        except Exception as e:
            logger.error(f"DataFrame conversion failed: {str(e)}")
            raise DataFrameConversionError(f"Conversion failed: {str(e)}")
    
    def _convert_single_object(
        self, 
        obj: CanvasObject, 
        object_type: str | None = None,
        flatten_nested: bool = True
    ) -> pd.DataFrame:
        """Convert a single Canvas object to DataFrame."""
        flattened = self._flatten_canvas_object(obj, flatten_nested)
        df = pd.DataFrame([flattened])
        
        # Apply schema optimization
        object_type = object_type or type(obj).__name__.lower()
        df = self._optimize_dataframe_schema(df, object_type)
        
        return df
    
    def _convert_object_list(
        self, 
        objects: list[CanvasObject], 
        object_type: str | None = None,
        flatten_nested: bool = True
    ) -> pd.DataFrame:
        """Convert a list of Canvas objects to DataFrame."""
        if not objects:
            return pd.DataFrame()
        
        # Determine object type from first object if not provided
        if not object_type:
            object_type = type(objects[0]).__name__.lower()
        
        # Process in batches for memory efficiency
        all_rows = []
        for i in range(0, len(objects), self.batch_size):
            batch = objects[i:i + self.batch_size]
            batch_rows = [self._flatten_canvas_object(obj, flatten_nested) for obj in batch]
            all_rows.extend(batch_rows)
            
            # Memory management
            if i > 0 and i % (self.batch_size * 5) == 0:
                gc.collect()
        
        df = pd.DataFrame(all_rows)
        df = self._optimize_dataframe_schema(df, object_type)
        
        return df
    
    def _convert_paginated_list(
        self, 
        paginated_list: PaginatedList, 
        object_type: str | None = None,
        flatten_nested: bool = True
    ) -> pd.DataFrame:
        """Convert PaginatedList to DataFrame with streaming processing."""
        try:
            rows = []
            object_count = 0
            inferred_type = None
            
            # Stream through paginated results
            for obj in paginated_list:
                # Infer object type from first object
                if inferred_type is None:
                    inferred_type = type(obj).__name__.lower()
                    object_type = object_type or inferred_type
                
                flattened = self._flatten_canvas_object(obj, flatten_nested)
                rows.append(flattened)
                object_count += 1
                
                # Process in batches to manage memory
                if len(rows) >= self.batch_size:
                    # Check memory usage periodically
                    if object_count % (self.batch_size * 2) == 0:
                        self._check_memory_usage()
                    
                    # Partial garbage collection
                    if object_count % (self.batch_size * 5) == 0:
                        gc.collect()
            
            if not rows:
                return pd.DataFrame()
            
            df = pd.DataFrame(rows)
            df = self._optimize_dataframe_schema(df, object_type)
            
            logger.info(f"Converted {object_count} {object_type} objects to DataFrame")
            return df
            
        except Exception as e:
            logger.error(f"PaginatedList conversion failed: {str(e)}")
            raise DataFrameConversionError(f"PaginatedList conversion failed: {str(e)}")
    
    def _flatten_canvas_object(self, obj: CanvasObject, flatten_nested: bool = True, depth: int = 0) -> dict:
        """
        Flatten a Canvas object into a dictionary suitable for DataFrame row.
        
        Args:
            obj: Canvas object to flatten
            flatten_nested: Whether to flatten nested objects
            depth: Current nesting depth
            
        Returns:
            Flattened dictionary representation
        """
        flattened = {}
        
        # Get all object attributes
        for attr_name, attr_value in obj.__dict__.items():
            if attr_name.startswith('_'):
                continue
            
            # Handle nested Canvas objects
            if isinstance(attr_value, CanvasObject) and flatten_nested and depth < self.max_depth:
                nested_flattened = self._flatten_canvas_object(attr_value, flatten_nested, depth + 1)
                for nested_key, nested_value in nested_flattened.items():
                    flattened[f"{attr_name}.{nested_key}"] = nested_value
            
            # Handle lists of Canvas objects
            elif isinstance(attr_value, list) and attr_value and isinstance(attr_value[0], CanvasObject):
                if flatten_nested and depth < self.max_depth:
                    # For lists, create summary fields
                    flattened[f"{attr_name}.count"] = len(attr_value)
                    if len(attr_value) > 0:
                        # Include first item as sample
                        first_item = self._flatten_canvas_object(attr_value[0], False, depth + 1)
                        for nested_key, nested_value in first_item.items():
                            flattened[f"{attr_name}.first.{nested_key}"] = nested_value
                else:
                    flattened[f"{attr_name}.count"] = len(attr_value)
            
            # Handle regular lists
            elif isinstance(attr_value, list):
                if len(attr_value) <= 10:  # Small lists as comma-separated strings
                    flattened[attr_name] = ', '.join(str(v) for v in attr_value)
                else:
                    flattened[f"{attr_name}.count"] = len(attr_value)
                    flattened[f"{attr_name}.sample"] = ', '.join(str(v) for v in attr_value[:3])
            
            # Handle dictionaries
            elif isinstance(attr_value, dict) and flatten_nested and depth < self.max_depth:
                for dict_key, dict_value in attr_value.items():
                    safe_key = str(dict_key).replace('.', '_')
                    flattened[f"{attr_name}.{safe_key}"] = dict_value
            
            # Handle primitive values
            else:
                flattened[attr_name] = attr_value
        
        return flattened
    
    def _optimize_dataframe_schema(self, df: pd.DataFrame, object_type: str) -> pd.DataFrame:
        """
        Optimize DataFrame schema with appropriate data types.
        
        Args:
            df: DataFrame to optimize
            object_type: Canvas object type for schema caching
            
        Returns:
            DataFrame with optimized dtypes
        """
        if df.empty:
            return df
        
        # Check schema cache
        cache_key = f"{object_type}_{len(df.columns)}"
        if cache_key in self._schema_cache:
            cached_schema = self._schema_cache[cache_key]
            return self._apply_cached_schema(df, cached_schema)
        
        optimized_df = df.copy()
        schema_info = {}
        
        for column in df.columns:
            try:
                # Analyze column data
                column_info = self._analyze_column(df[column], column)
                schema_info[column] = column_info
                
                # Apply optimized dtype
                if column_info['dtype'] != 'object':
                    optimized_df[column] = self._convert_column_dtype(df[column], column_info)
                    
            except Exception as e:
                logger.warning(f"Column optimization failed for {column}: {str(e)}")
                # Keep original dtype on failure
                pass
        
        # Cache the schema for future use
        self._schema_cache[cache_key] = schema_info
        
        return optimized_df
    
    def _analyze_column(self, series: pd.Series, column_name: str) -> dict[str, str | bool]:
        """Analyze a column to determine optimal data type."""
        non_null_series = series.dropna()
        
        if len(non_null_series) == 0:
            return {'dtype': 'object', 'nullable': True}
        
        # Check for ID columns
        if any(id_pattern in column_name.lower() for id_pattern in ['id', '_id', 'uuid']):
            # Determine if numeric or string ID
            if non_null_series.dtype in ['int64', 'int32'] or all(str(v).isdigit() for v in non_null_series.head(100)):
                return {'dtype': 'Int64', 'nullable': True}  # Nullable integer
            else:
                return {'dtype': 'string', 'nullable': True}
        
        # Check for datetime columns
        if any(date_pattern in column_name.lower() for date_pattern in ['date', 'time', 'created', 'updated', 'due']):
            if self._is_datetime_column(non_null_series):
                return {'dtype': 'datetime64[ns]', 'nullable': True}
        
        # Check for boolean columns
        if self._is_boolean_column(non_null_series):
            return {'dtype': 'boolean', 'nullable': True}
        
        # Check for numeric columns
        if pd.api.types.is_numeric_dtype(non_null_series):
            if non_null_series.dtype == 'float64':
                # Check if can be integer
                if non_null_series.notna().all() and (non_null_series % 1 == 0).all():
                    return {'dtype': 'Int64', 'nullable': True}
                else:
                    return {'dtype': 'float64', 'nullable': True}
            else:
                return {'dtype': 'Int64', 'nullable': True}
        
        # Default to string for text data
        return {'dtype': 'string', 'nullable': True}
    
    def _is_datetime_column(self, series: pd.Series) -> bool:
        """Check if a series contains datetime data."""
        sample = series.head(min(100, len(series)))
        datetime_count = 0
        
        for value in sample:
            if pd.isna(value):
                continue
            try:
                pd.to_datetime(str(value))
                datetime_count += 1
            except (ValueError, TypeError):
                pass
        
        return datetime_count / len(sample.dropna()) > 0.8
    
    def _is_boolean_column(self, series: pd.Series) -> bool:
        """Check if a series contains boolean data."""
        unique_values = set(str(v).lower() for v in series.dropna().unique())
        boolean_values = {'true', 'false', '1', '0', 'yes', 'no', 't', 'f'}
        return len(unique_values) <= 2 and unique_values.issubset(boolean_values)
    
    def _convert_column_dtype(self, series: pd.Series, column_info: dict) -> pd.Series:
        """Convert a series to the specified dtype."""
        target_dtype = column_info['dtype']
        
        try:
            if target_dtype == 'datetime64[ns]':
                return pd.to_datetime(series, errors='coerce')
            elif target_dtype == 'boolean':
                return series.map(self._convert_to_boolean).astype('boolean')
            elif target_dtype == 'Int64':
                return pd.to_numeric(series, errors='coerce').astype('Int64')
            elif target_dtype == 'float64':
                return pd.to_numeric(series, errors='coerce')
            elif target_dtype == 'string':
                return series.astype('string')
            else:
                return series
        except Exception as e:
            logger.warning(f"Dtype conversion failed: {str(e)}")
            return series
    
    def _convert_to_boolean(self, value) -> bool | None:
        """Convert value to boolean."""
        if pd.isna(value):
            return None
        
        str_value = str(value).lower().strip()
        if str_value in ['true', '1', 'yes', 't', 'y']:
            return True
        elif str_value in ['false', '0', 'no', 'f', 'n']:
            return False
        else:
            return None
    
    def _apply_cached_schema(self, df: pd.DataFrame, schema_info: dict) -> pd.DataFrame:
        """Apply cached schema information to DataFrame."""
        optimized_df = df.copy()
        
        for column, info in schema_info.items():
            if column in df.columns and info['dtype'] != 'object':
                try:
                    optimized_df[column] = self._convert_column_dtype(df[column], info)
                except Exception as e:
                    logger.warning(f"Cached schema application failed for {column}: {str(e)}")
        
        return optimized_df
    
    def _check_memory_usage(self):
        """Check current memory usage and warn if approaching limits."""
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            if memory_mb > self.memory_limit_mb:
                logger.warning(f"Memory usage ({memory_mb:.1f}MB) exceeds limit ({self.memory_limit_mb}MB)")
                gc.collect()
        except ImportError:
            # psutil not available, skip memory checking
            pass
    
    def get_dataframe_info(self, df: pd.DataFrame) -> dict:
        """
        Get comprehensive information about a DataFrame.
        
        Args:
            df: DataFrame to analyze
            
        Returns:
            Dictionary containing DataFrame metadata
        """
        return {
            'shape': df.shape,
            'columns': list(df.columns),
            'dtypes': df.dtypes.to_dict(),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'null_counts': df.isnull().sum().to_dict(),
            'sample_data': df.head(3).to_dict('records') if not df.empty else []
        }
    
    def export_to_formats(self, df: pd.DataFrame) -> dict:
        """
        Export DataFrame to multiple formats for MCP responses.
        
        Args:
            df: DataFrame to export
            
        Returns:
            Dictionary containing different format representations
        """
        formats = {}
        
        try:
            # JSON format (with proper datetime handling)
            formats['json'] = df.to_dict('records')
            
            # CSV format (as string)
            formats['csv'] = df.to_csv(index=False)
            
            # Summary statistics
            if not df.empty:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    formats['summary_stats'] = df[numeric_cols].describe().to_dict()
            
            # Basic info
            formats['info'] = self.get_dataframe_info(df)
            
        except Exception as e:
            logger.error(f"Format export failed: {str(e)}")
            formats['error'] = str(e)
        
        return formats
    
    def clear_caches(self):
        """Clear all internal caches."""
        self._schema_cache.clear()
        self._type_cache.clear()
        logger.info("DataFrame converter caches cleared")


# Global converter instance
converter = DataFrameConverter()


def convert_to_dataframe(
    data: CanvasObject | list[CanvasObject] | PaginatedList,
    **kwargs
) -> pd.DataFrame:
    """
    Convenience function for DataFrame conversion.
    
    Args:
        data: Canvas data to convert
        **kwargs: Additional conversion options
        
    Returns:
        pandas DataFrame
    """
    return converter.convert_to_dataframe(data, **kwargs)


def get_dataframe_info(df: pd.DataFrame) -> dict:
    """
    Convenience function for DataFrame information.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        DataFrame metadata dictionary
    """
    return converter.get_dataframe_info(df)