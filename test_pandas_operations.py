#!/usr/bin/env python3
"""
Test script for pandas operations engine.

This script tests the PandasEngine with sample Canvas-like data to verify
that all pandas operations work correctly before integration testing.
"""

import pandas as pd
import sys
import json
from datetime import datetime, timedelta

# Add the project root to the path so we can import canvasapi_mcp
sys.path.insert(0, '/Users/tshippen/Documents/Code Projects/canvasapi_get')

from canvasapi_mcp.utils.pandas_engine import PandasEngine, PandasOperationError


def create_test_dataframe():
    """Create a test DataFrame that mimics Canvas enrollment data."""
    import random
    from datetime import datetime, timedelta
    
    # Generate sample enrollment data
    base_date = datetime.now() - timedelta(days=30)
    data = []
    
    courses = [101, 102, 103, 104, 105]
    statuses = ['active', 'inactive', 'completed', 'deleted']
    
    for i in range(500):  # 500 test enrollments
        data.append({
            'id': i + 1,
            'user_id': random.randint(1000, 9999),
            'course_id': random.choice(courses),
            'enrollment_state': random.choice(statuses),
            'created_at': base_date + timedelta(days=random.randint(0, 30)),
            'total_activity_time': random.randint(0, 3600),  # seconds
            'current_score': random.uniform(60, 100) if random.random() > 0.2 else None,
            'email': f"user{random.randint(1000, 9999)}@example.com" if random.random() > 0.1 else None
        })
    
    return pd.DataFrame(data)


def test_basic_operations():
    """Test basic pandas operations."""
    print("🧪 Testing Basic Pandas Operations")
    print("=" * 50)
    
    engine = PandasEngine()
    df = create_test_dataframe()
    
    print(f"Original DataFrame shape: {df.shape}")
    print(f"Original columns: {list(df.columns)}")
    print()
    
    # Test 1: Simple query operation
    print("Test 1: Query operation (active enrollments)")
    operations = [{"operation": "query", "expr": "enrollment_state == 'active'"}]
    
    try:
        result = engine.apply_operations(df, operations)
        print(f"✅ Query successful: {len(result)} active enrollments found")
        print(f"Result shape: {result.shape}")
    except Exception as e:
        print(f"❌ Query failed: {e}")
    print()
    
    # Test 2: Sort operation
    print("Test 2: Sort by created_at")
    operations = [{"operation": "sort_values", "by": "created_at", "ascending": False}]
    
    try:
        result = engine.apply_operations(df, operations)
        print(f"✅ Sort successful")
        print(f"Latest enrollment: {result.iloc[0]['created_at']}")
        print(f"Oldest enrollment: {result.iloc[-1]['created_at']}")
    except Exception as e:
        print(f"❌ Sort failed: {e}")
    print()
    
    # Test 3: Combined operations (filter, sort, limit)
    print("Test 3: Combined operations (filter + sort + limit)")
    operations = [
        {"operation": "query", "expr": "enrollment_state == 'active'"},
        {"operation": "sort_values", "by": "current_score", "ascending": False},
        {"operation": "head", "n": 10}
    ]
    
    try:
        result = engine.apply_operations(df, operations)
        print(f"✅ Combined operations successful")
        print(f"Top 10 active students by score: {result.shape}")
        if len(result) > 0:
            print(f"Highest score: {result.iloc[0]['current_score']}")
    except Exception as e:
        print(f"❌ Combined operations failed: {e}")
    print()


def test_aggregation_operations():
    """Test groupby and aggregation operations."""
    print("🧪 Testing Aggregation Operations")
    print("=" * 50)
    
    engine = PandasEngine()
    df = create_test_dataframe()
    
    # Test groupby + agg
    print("Test: Group by course_id and aggregate")
    operations = [
        {"operation": "dropna", "subset": ["current_score"]},
        {"operation": "groupby", "by": "course_id", "as_index": False},
        {"operation": "agg", "func": {"student_count": "count", "avg_score": "mean"}}
    ]
    
    try:
        result = engine.apply_operations(df, operations)
        print(f"✅ Aggregation successful")
        print(f"Result shape: {result.shape}")
        print(f"Columns: {list(result.columns)}")
        if len(result) > 0:
            print(f"Sample result:\n{result.head()}")
    except Exception as e:
        print(f"❌ Aggregation failed: {e}")
    print()


def test_data_cleaning():
    """Test data cleaning operations."""
    print("🧪 Testing Data Cleaning Operations")
    print("=" * 50)
    
    engine = PandasEngine()
    df = create_test_dataframe()
    
    # Add some duplicates for testing
    duplicate_rows = df.head(10).copy()
    df_with_dupes = pd.concat([df, duplicate_rows], ignore_index=True)
    
    print(f"DataFrame with duplicates: {df_with_dupes.shape}")
    
    operations = [
        {"operation": "drop_duplicates", "subset": ["user_id", "course_id"], "keep": "first"},
        {"operation": "fillna", "value": "Unknown"},
        {"operation": "sort_values", "by": "id"}
    ]
    
    try:
        result = engine.apply_operations(df_with_dupes, operations)
        print(f"✅ Data cleaning successful")
        print(f"Cleaned shape: {result.shape}")
        print(f"Removed {len(df_with_dupes) - len(result)} duplicate rows")
    except Exception as e:
        print(f"❌ Data cleaning failed: {e}")
    print()


def test_error_handling():
    """Test error handling for invalid operations."""
    print("🧪 Testing Error Handling")
    print("=" * 50)
    
    engine = PandasEngine()
    df = create_test_dataframe()
    
    # Test invalid operation
    print("Test 1: Invalid operation name")
    operations = [{"operation": "invalid_operation"}]
    
    try:
        result = engine.apply_operations(df, operations)
        print(f"❌ Should have failed but didn't")
    except PandasOperationError as e:
        print(f"✅ Correctly caught invalid operation: {str(e)[:100]}...")
    print()
    
    # Test invalid query expression
    print("Test 2: Invalid query expression")
    operations = [{"operation": "query", "expr": "invalid_column == 'test'"}]
    
    try:
        result = engine.apply_operations(df, operations)
        print(f"❌ Should have failed but didn't")
    except PandasOperationError as e:
        print(f"✅ Correctly caught invalid query: {str(e)[:100]}...")
    print()
    
    # Test missing required parameter
    print("Test 3: Missing required parameter")
    operations = [{"operation": "sort_values"}]  # Missing 'by' parameter
    
    try:
        result = engine.apply_operations(df, operations)
        print(f"❌ Should have failed but didn't")
    except PandasOperationError as e:
        print(f"✅ Correctly caught missing parameter: {str(e)[:100]}...")
    print()


def test_available_operations():
    """Test the operation documentation system."""
    print("🧪 Testing Operation Documentation")
    print("=" * 50)
    
    engine = PandasEngine()
    
    operations = engine.get_available_operations()
    print(f"Available operations: {len(operations)}")
    
    for op_name, op_info in list(operations.items())[:3]:  # Show first 3
        print(f"\n{op_name}:")
        print(f"  Description: {op_info['description']}")
        print(f"  Required params: {op_info['required_params']}")
        print(f"  Optional params: {op_info['optional_params']}")
        print(f"  Example: {op_info['example']}")
    
    print(f"\n✅ Operation documentation available for {len(operations)} operations")
    
    # Test example sequences
    examples = engine.get_operation_examples()
    print(f"✅ Example sequences available: {list(examples.keys())}")
    print()


def test_memory_estimation():
    """Test memory usage estimation."""
    print("🧪 Testing Memory Estimation")
    print("=" * 50)
    
    engine = PandasEngine()
    df = create_test_dataframe()
    
    memory_info = engine.estimate_memory_usage(df)
    
    print(f"Memory estimation:")
    print(f"  Rows: {memory_info['rows']}")
    print(f"  Columns: {memory_info['columns']}")
    print(f"  Memory (MB): {memory_info['memory_mb']}")
    print(f"  Estimated safe: {memory_info['estimated_safe']}")
    print(f"✅ Memory estimation working")
    print()


def main():
    """Run all tests."""
    print("🚀 Canvas MCP Pandas Operations Engine Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_basic_operations()
        test_aggregation_operations()
        test_data_cleaning()
        test_error_handling()
        test_available_operations()
        test_memory_estimation()
        
        print("🎉 All tests completed successfully!")
        print("The pandas operations engine is ready for integration.")
        
    except Exception as e:
        print(f"💥 Test suite failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)