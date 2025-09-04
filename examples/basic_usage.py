"""
Basic usage examples for splurge-typer.

This example demonstrates the fundamental usage patterns of the splurge-typer library,
including single value inference, type conversion, and basic collection analysis.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from splurge_typer import TypeInference


def main():
    """Demonstrate basic usage of splurge-typer."""

    print("=== splurge-typer Basic Usage Examples ===\n")

    # Create a TypeInference instance
    ti = TypeInference()

    # Example 1: Single value type inference
    print("1. Single Value Type Inference:")
    examples = [
        ("123", "Integer"),
        ("-456", "Negative integer"),
        ("123.45", "Float"),
        ("-789.12", "Negative float"),
        ("true", "Boolean (true)"),
        ("False", "Boolean (false)"),
        ("2023-01-01", "Date"),
        ("14:30:00", "Time"),
        ("2023-01-01T12:00:00", "DateTime (ISO format)"),
        ("2023-01-01 12:00:00", "DateTime (space separated)"),
        ("hello world", "String"),
        ("", "Empty string"),
        ("   ", "Whitespace string"),
        ("none", "None value"),
        ("null", "Null value"),
    ]

    for value, description in examples:
        inferred_type = ti.infer_type(value)
        print(f"  '{value}' ({description}) -> {inferred_type.value}")

    print()

    # Example 2: Type conversion
    print("2. Type Conversion:")
    conversion_examples = [
        ("123", "Integer conversion"),
        ("123.45", "Float conversion"),
        ("true", "Boolean conversion"),
        ("2023-01-01", "Date conversion"),
        ("14:30:00", "Time conversion"),
        ("2023-01-01T12:00:00", "DateTime conversion (ISO)"),
        ("2023-01-01 12:00:00", "DateTime conversion (space)"),
    ]

    for value, _description in conversion_examples:
        converted = ti.convert_value(value)
        print(f"  '{value}' -> {converted} ({type(converted).__name__})")

    print()

    # Example 3: Collection analysis
    print("3. Collection Analysis:")

    collections = [
        (["1", "2", "3", "4", "5"], "Integer collection"),
        (["1.1", "2.2", "3.3"], "Float collection"),
        (["true", "false", "True", "False"], "Boolean collection"),
        (["2023-01-01", "2023-01-02", "2023-01-03"], "Date collection"),
        (["hello", "world", "python"], "String collection"),
        (["1", "2.5", "hello", "true"], "Mixed collection"),
        ([], "Empty collection"),
    ]

    for values, description in collections:
        profile = ti.profile_values(values)
        print(f"  {description}: {profile.value} ({len(values)} items)")

    print()

    # Example 4: Practical use cases
    print("4. Practical Use Cases:")

    # CSV-like data processing
    print("  CSV Data Processing:")
    csv_headers = ["id", "name", "age", "salary", "active"]
    csv_row = ["1", "John Doe", "30", "50000.00", "true"]

    print(f"    Headers: {csv_headers}")
    print(f"    Row: {csv_row}")

    # Convert each field
    converted_row = []
    for i, value in enumerate(csv_row):
        converted = ti.convert_value(value)
        field_type = type(converted).__name__
        print(f"    {csv_headers[i]}: '{value}' -> {converted} ({field_type})")
        converted_row.append(converted)

    print(f"    Converted row: {converted_row}")

    print()

    # JSON-like data processing
    print("  JSON Data Processing:")
    json_data = {
        "user_id": "12345",
        "username": "johndoe",
        "age": "30",
        "balance": "1234.56",
        "is_active": "true",
        "last_login": "2023-12-01T10:30:00"
    }

    print("    Original JSON-like data:")
    for key, value in json_data.items():
        print(f"      {key}: '{value}'")

    print("    Processed data:")
    processed_data = {}
    for key, value in json_data.items():
        converted = ti.convert_value(value)
        field_type = type(converted).__name__
        print(f"      {key}: {converted} ({field_type})")
        processed_data[key] = converted

    print(f"    Final processed data: {processed_data}")

    print("\n=== Examples Complete ===")


if __name__ == "__main__":
    main()
