"""
Advanced usage examples for splurge-typer.

This example demonstrates advanced features including performance optimization,
error handling, edge cases, and real-world data processing scenarios.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

import time

from splurge_typer import DataType, String, TypeInference


def benchmark_operation(operation_name, operation_func, iterations=1000):
    """Benchmark an operation and return average execution time."""
    start_time = time.time()
    for _ in range(iterations):
        operation_func()
    end_time = time.time()
    avg_time = (end_time - start_time) / iterations
    print(f"Average time: {avg_time:.6f}")
    return avg_time


def main():
    """Demonstrate advanced usage of splurge-typer."""

    print("=== splurge-typer Advanced Usage Examples ===\n")

    ti = TypeInference()

    # Example 1: Performance optimization with large datasets
    print("1. Performance Optimization:")

    # Check incremental processing threshold
    threshold = TypeInference.get_incremental_typecheck_threshold()
    print(f"   Incremental processing threshold: {threshold} items")

    # Small dataset
    small_dataset = [str(i) for i in range(100)]
    print(f"   Small dataset ({len(small_dataset)} items): ", end="")
    profile = ti.profile_values(small_dataset)
    print(f"{profile.value}")

    # Large dataset
    large_dataset = [str(i) for i in range(50000)]
    print(f"   Large dataset ({len(large_dataset)} items): ", end="")
    start_time = time.time()
    profile = ti.profile_values(large_dataset)
    end_time = time.time()
    print(f"{end_time - start_time:.4f}s")
    print()

    # Example 2: Edge cases and error handling
    print("2. Edge Cases and Error Handling:")

    edge_cases = [
        ("", "Empty string"),
        ("   ", "Whitespace only"),
        ("none", "None representation"),
        ("null", "Null representation"),
        ("00123", "Leading zeros (integer)"),
        ("00123.4500", "Leading zeros (float)"),
        ("1.23e10", "Scientific notation"),
        ("25:00:00", "Invalid time (hour > 24)"),
        ("2023-13-01", "Invalid date (month > 12)"),
        ("not-a-date", "Invalid date format"),
        ("true", "Boolean true"),
        ("false", "Boolean false"),
        ("TRUE", "Boolean TRUE (uppercase)"),
        ("False", "Boolean False (mixed case)"),
        ("1", "Boolean 1"),
        ("0", "Boolean 0"),
        ("yes", "Boolean yes"),
        ("no", "Boolean no"),
    ]

    for value, description in edge_cases:
        inferred_type = ti.infer_type(value)
        converted = ti.convert_value(value)
        print(f"   '{value}' ({description}):")
        print(f"     Type: {inferred_type.value}")
        print(f"     Converted: {converted} ({type(converted).__name__})")

    print()

    # Example 3: Multiple date and time formats
    print("3. Multiple Date and Time Formats:")

    date_formats = [
        ("2023-01-01", "ISO format"),
        ("01/01/2023", "US format"),
        ("01.01.2023", "Dot format"),
        ("20230101", "Compact format"),
        ("01-01-2023", "Dash US format"),
    ]

    print("   Date formats:")
    for date_str, format_name in date_formats:
        inferred = ti.infer_type(date_str)
        converted = ti.convert_value(date_str)
        print(f"     '{date_str}' ({format_name}): {converted}")

    time_formats = [
        ("14:30:00", "24-hour format"),
        ("2:30 PM", "12-hour format"),
        ("14:30", "Short 24-hour"),
        ("143000", "Compact format"),
    ]

    print("   Time formats:")
    for time_str, format_name in time_formats:
        inferred = ti.infer_type(time_str)
        converted = ti.convert_value(time_str)
        print(f"     '{time_str}' ({format_name}): {converted}")

    datetime_formats = [
        ("2023-01-01T12:00:00", "ISO datetime"),
        ("2023-01-01 12:00:00", "Space separated"),
        ("01/01/2023 12:00:00", "US datetime"),
    ]

    print("   DateTime formats:")
    for dt_str, format_name in datetime_formats:
        inferred = ti.infer_type(dt_str)
        converted = ti.convert_value(dt_str)
        print(f"     '{dt_str}' ({format_name}): {converted}")

    print()

    # Example 4: Data quality analysis
    print("4. Data Quality Analysis:")

    # Simulate messy real-world data
    messy_data = [
        "123",      # Valid integer
        "  456  ",  # Integer with whitespace
        "789.12",   # Valid float
        "abc",      # Invalid - string
        "",         # Empty
        "   ",      # Whitespace only
        "true",     # Valid boolean
        "2023-01-01",  # Valid date
        "not-a-date",  # Invalid date
        "25:00:00",    # Invalid time
    ]

    print("   Analyzing messy dataset:")
    print(f"   Original data: {messy_data}")

    # Analyze each value
    analysis_results = []
    for value in messy_data:
        inferred_type = ti.infer_type(value)
        can_infer = TypeInference.can_infer(value)
        analysis_results.append({
            'value': value,
            'type': inferred_type.value,
            'can_infer': can_infer
        })

    # Group by type
    type_counts = {}
    for result in analysis_results:
        type_name = result['type']
        type_counts[type_name] = type_counts.get(type_name, 0) + 1

    print("   Type distribution:")
    for type_name, count in type_counts.items():
        percentage = (count / len(messy_data)) * 100
        print(f"     {type_name}: {count} ({percentage:.1f}%)")
    # Show detailed analysis
    print("   Detailed analysis:")
    for result in analysis_results:
        status = "✓" if result['can_infer'] else "✗"
        print(f"     '{result['value']}': {result['type']} {status}")

    print()

    # Example 5: Batch processing comparison
    print("5. Batch Processing Scenarios:")

    # Create different types of datasets
    datasets = {
        "Integers": [str(i) for i in range(1000)],
        "Floats": [f"{i}.{i}" for i in range(1000)],
        "Booleans": ["true", "false"] * 500,
        "Mixed": ["123", "45.67", "true", "hello"] * 250,
    }

    print("   Dataset analysis:")
    for name, data in datasets.items():
        start_time = time.time()
        profile = ti.profile_values(data)
        end_time = time.time()
        processing_time = end_time - start_time
        print(f"     {name}: {profile} ({processing_time:.6f}s)")
    print()

    # Example 6: String utility functions
    print("6. String Utility Functions:")

    test_values = [
        ("123", "Integer"),
        ("45.67", "Float"),
        ("true", "Boolean"),
        ("2023-01-01", "Date"),
        ("14:30:00", "Time"),
        ("hello", "String"),
    ]

    print("   String validation and conversion:")
    for value, expected_type in test_values:
        # Test validation methods
        is_int = String.is_int_like(value)
        is_float = String.is_float_like(value)
        is_bool = String.is_bool_like(value)
        is_date = String.is_date_like(value)
        is_time = String.is_time_like(value)

        # Test direct inference
        inferred = String.infer_type(value)

        # Test conversion
        if inferred == DataType.INTEGER:
            converted = String.to_int(value)
        elif inferred == DataType.FLOAT:
            converted = String.to_float(value)
        elif inferred == DataType.BOOLEAN:
            converted = String.to_bool(value)
        elif inferred == DataType.DATE:
            converted = String.to_date(value)
        elif inferred == DataType.TIME:
            converted = String.to_time(value)
        else:
            converted = value

        print(f"     '{value}' ({expected_type}):")
        print(f"       Validation: int={is_int}, float={is_float}, bool={is_bool}, date={is_date}, time={is_time}")
        print(f"       Inference: {inferred.value}")
        print(f"       Conversion: {converted} ({type(converted).__name__})")

    print()

    # Example 7: Static vs Instance methods
    print("7. Static vs Instance Method Comparison:")

    test_value = "12345"

    # Instance methods
    print("   Instance methods:")
    instance_type = ti.infer_type(test_value)
    instance_converted = ti.convert_value(test_value)
    print(f"     infer_type: {instance_type.value}")
    print(f"     convert_value: {instance_converted}")

    # Static methods
    print("   Static methods:")
    static_can_infer = TypeInference.can_infer(test_value)
    static_threshold = TypeInference.get_incremental_typecheck_threshold()
    print(f"     can_infer: {static_can_infer}")
    print(f"     threshold: {static_threshold}")

    # Direct String methods
    print("   Direct String methods:")
    string_inferred = String.infer_type(test_value)
    string_converted = String.to_int(test_value)
    print(f"     String.infer_type: {string_inferred.value}")
    print(f"     String.to_int: {string_converted}")

    print("\n=== Advanced Examples Complete ===")


if __name__ == "__main__":
    main()
