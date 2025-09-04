"""
Performance benchmarking examples for splurge-typer.

This example demonstrates performance characteristics of the library with various
dataset sizes and types, including benchmarking utilities and optimization tips.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

import statistics
import time
from collections.abc import Callable

from splurge_typer import TypeInference


class BenchmarkTimer:
    """Simple benchmarking utility."""

    def __init__(self, name: str):
        self.name = name
        self.start_time = None
        self.end_time = None

    def __enter__(self):
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()

    @property
    def elapsed_time(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None or self.end_time is None:
            return 0.0
        return self.end_time - self.start_time

    def print_result(self):
        """Print benchmark result."""
        print(f"{self.elapsed_time:.6f}s")


def benchmark_function(func: Callable, iterations: int = 100) -> float:
    """Benchmark a function over multiple iterations."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        end = time.perf_counter()
        times.append(end - start)

    avg_time = statistics.mean(times)
    std_dev = statistics.stdev(times) if len(times) > 1 else 0

    print(f"{avg_time:.6f}s")
    return avg_time


def create_test_dataset(size: int, data_type: str) -> list[str]:
    """Create a test dataset of specified size and type."""
    if data_type == "integer":
        return [str(i) for i in range(size)]
    elif data_type == "float":
        return [f"{i}.{i % 100}" for i in range(size)]
    elif data_type == "boolean":
        return ["true", "false"] * (size // 2)
    elif data_type == "string":
        return [f"string_{i}" for i in range(size)]
    elif data_type == "date":
        return [f"2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}" for i in range(size)]
    elif data_type == "mixed":
        base_size = size // 5
        result = []
        result.extend([str(i) for i in range(base_size)])  # integers
        result.extend([f"{i}.{i % 100}" for i in range(base_size)])  # floats
        result.extend(["true", "false"] * (base_size // 2))  # booleans
        result.extend([f"string_{i}" for i in range(base_size)])  # strings
        result.extend([f"2023-01-{(i % 28) + 1:02d}" for i in range(size - len(result))])  # dates
        return result
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def main():
    """Run performance benchmarks."""

    print("=== splurge-typer Performance Benchmarks ===\n")

    ti = TypeInference()

    # Example 1: Single value operations
    print("1. Single Value Operations:")

    test_values = [
        ("123", "Integer"),
        ("123.45", "Float"),
        ("true", "Boolean"),
        ("2023-01-01", "Date"),
        ("14:30:00", "Time"),
        ("hello world", "String"),
    ]

    print("   Single value inference benchmark:")
    for value, desc in test_values:
        avg_time = benchmark_function(lambda: ti.infer_type(value), iterations=1000)
        inferred = ti.infer_type(value)
        print(f"     {desc} '{value}': {inferred.value}")

    print("   Single value conversion benchmark:")
    for value, desc in test_values:
        avg_time = benchmark_function(lambda: ti.convert_value(value), iterations=1000)
        converted = ti.convert_value(value)
        print(f"     {desc} '{value}': {type(converted).__name__}")

    print()

    # Example 2: Collection analysis with different sizes
    print("2. Collection Analysis - Size Scaling:")

    sizes = [100, 1000, 10000, 50000]

    for size in sizes:
        dataset = create_test_dataset(size, "integer")

        with BenchmarkTimer(f"Integer collection ({size} items)") as timer:
            profile = ti.profile_values(dataset)

        timer.print_result()
        print(f"     Result: {profile.value}")

    print()

    # Example 3: Different data types performance
    print("3. Different Data Types Performance:")

    data_types = ["integer", "float", "boolean", "string", "date", "mixed"]
    test_size = 5000

    for data_type in data_types:
        dataset = create_test_dataset(test_size, data_type)

        with BenchmarkTimer(f"{data_type.capitalize()} ({test_size} items)") as timer:
            profile = ti.profile_values(dataset)

        timer.print_result()
        print(f"     Result: {profile.value}")

    print()

    # Example 4: Incremental processing threshold analysis
    print("4. Incremental Processing Analysis:")

    threshold = TypeInference.get_incremental_typecheck_threshold()
    print(f"   Incremental threshold: {threshold} items")

    # Test around the threshold
    test_sizes = [threshold - 1000, threshold, threshold + 1000]

    for size in test_sizes:
        if size <= 0:
            continue

        dataset = create_test_dataset(size, "integer")

        with BenchmarkTimer(f"Threshold test ({size} items)") as timer:
            profile = ti.profile_values(dataset)

        timer.print_result()
        is_incremental = "Yes" if size >= threshold else "No"
        print(f"     Uses incremental: {is_incremental}")

    print()

    # Example 5: Memory efficiency test
    print("5. Memory Efficiency Test:")

    # Test with very large dataset
    large_size = 100000
    print(f"   Creating large dataset ({large_size} items)...")

    dataset = create_test_dataset(large_size, "integer")

    print(f"   Dataset created. Memory usage: ~{len(dataset) * 10} bytes for strings")

    with BenchmarkTimer(f"Large dataset processing ({large_size} items)") as timer:
        profile = ti.profile_values(dataset)

    timer.print_result()
    print(f"     Result: {profile.value}")

    # Test memory cleanup
    del dataset
    print("   Dataset cleaned up")

    print()

    # Example 6: Batch processing optimization
    print("6. Batch Processing Optimization:")

    # Compare processing individual values vs. collection
    test_values = [str(i) for i in range(1000)]

    # Individual processing
    with BenchmarkTimer("Individual processing (1000 items)") as timer:
        individual_results = []
        for value in test_values:
            individual_results.append(ti.infer_type(value))

    timer.print_result()

    # Collection processing
    with BenchmarkTimer("Collection processing (1000 items)") as timer:
        collection_result = ti.profile_values(test_values)

    timer.print_result()
    print(f"     Collection result: {collection_result.value}")

    print()

    # Example 7: Real-world scenario simulation
    print("7. Real-World Scenario Simulation:")

    # Simulate CSV processing
    print("   CSV Processing Simulation:")

    # Create simulated CSV data (10 columns x 1000 rows)
    num_rows = 1000
    csv_data = []

    for i in range(num_rows):
        row = [
            str(i),                          # ID (integer)
            f"User_{i}",                     # Name (string)
            str(20 + (i % 50)),             # Age (integer)
            f"{50000 + i * 1.23:.2f}",       # Salary (float)
            ["true", "false"][i % 2],       # Active (boolean)
            f"2023-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",  # Hire date (date)
        ]
        csv_data.append(row)

    # Process each column
    columns = list(zip(*csv_data, strict=False))  # Transpose to get columns

    column_names = ["ID", "Name", "Age", "Salary", "Active", "Hire_Date"]
    expected_types = ["int", "str", "int", "float", "bool", "date"]

    with BenchmarkTimer(f"CSV processing ({num_rows} rows x {len(column_names)} columns)") as timer:
        for i, (column_name, column_data) in enumerate(zip(column_names, columns, strict=False)):
            profile = ti.profile_values(column_data)
            print(f"     Column {column_name}: {profile.value} (expected: {expected_types[i]})")

    timer.print_result()

    print()

    # Example 8: Performance tips
    print("8. Performance Optimization Tips:")
    print("   - Use collection analysis (profile_values) for bulk operations")
    print("   - Large datasets (>10,000 items) automatically use incremental processing")
    print("   - Convert values only when needed - inference is faster")
    print("   - Cache TypeInference instances for repeated use")
    print("   - Use appropriate data types to minimize conversion overhead")
    print("   - Consider memory usage for very large datasets (>100,000 items)")

    print("\n=== Performance Benchmarks Complete ===")


if __name__ == "__main__":
    main()
