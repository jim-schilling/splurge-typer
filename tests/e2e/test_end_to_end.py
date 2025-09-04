"""
End-to-end tests for splurge-typer library.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from datetime import date, datetime

from splurge_typer import DataType, TypeInference


class TestEndToEndScenarios:
    """End-to-end test scenarios simulating real-world usage."""

    def test_csv_data_processing_scenario(self):
        """Test processing CSV-like data."""
        ti = TypeInference()

        # Simulate CSV headers and data
        _headers = ["id", "name", "age", "salary", "active", "hire_date"]
        row1 = ["1", "John Doe", "30", "50000.00", "true", "2020-01-15"]
        row2 = ["2", "Jane Smith", "25", "45000.50", "false", "2021-03-20"]
        row3 = ["3", "Bob Johnson", "35", "55000.25", "true", "2019-11-10"]

        # Analyze each column
        columns = list(zip(*[row1, row2, row3], strict=False))

        # ID column (integers)
        id_types = [ti.infer_type(id_val) for id_val in columns[0]]
        assert all(t == DataType.INTEGER for t in id_types)

        # Name column (strings)
        name_types = [ti.infer_type(name) for name in columns[1]]
        assert all(t == DataType.STRING for t in name_types)

        # Age column (integers)
        age_types = [ti.infer_type(age) for age in columns[2]]
        assert all(t == DataType.INTEGER for t in age_types)

        # Salary column (floats)
        salary_types = [ti.infer_type(salary) for salary in columns[3]]
        assert all(t == DataType.FLOAT for t in salary_types)

        # Active column (booleans)
        active_types = [ti.infer_type(active) for active in columns[4]]
        assert all(t == DataType.BOOLEAN for t in active_types)

        # Hire date column (dates)
        hire_date_types = [ti.infer_type(date_str) for date_str in columns[5]]
        assert all(t == DataType.DATE for t in hire_date_types)

        # Convert sample row
        converted_row1 = [ti.convert_value(val) for val in row1]
        expected_row1 = [
            1, "John Doe", 30, 50000.00, True,
            date(2020, 1, 15)
        ]
        assert converted_row1 == expected_row1

    def test_json_data_processing_scenario(self):
        """Test processing JSON-like data structures."""
        ti = TypeInference()

        # Simulate JSON data
        json_like_data = {
            "users": [
                {
                    "id": "1",
                    "name": "Alice",
                    "age": "28",
                    "balance": "1234.56",
                    "is_active": "true",
                    "last_login": "2023-12-01T10:30:00"
                },
                {
                    "id": "2",
                    "name": "Bob",
                    "age": "34",
                    "balance": "789.12",
                    "is_active": "false",
                    "last_login": "2023-11-15T14:20:00"
                }
            ]
        }

        # Process user data
        for user in json_like_data["users"]:
            # ID should be integer
            assert ti.infer_type(user["id"]) == DataType.INTEGER
            assert isinstance(ti.convert_value(user["id"]), int)

            # Name should be string
            assert ti.infer_type(user["name"]) == DataType.STRING
            assert isinstance(ti.convert_value(user["name"]), str)

            # Age should be integer
            assert ti.infer_type(user["age"]) == DataType.INTEGER
            assert isinstance(ti.convert_value(user["age"]), int)

            # Balance should be float
            assert ti.infer_type(user["balance"]) == DataType.FLOAT
            assert isinstance(ti.convert_value(user["balance"]), float)

            # Active should be boolean
            assert ti.infer_type(user["is_active"]) == DataType.BOOLEAN
            assert isinstance(ti.convert_value(user["is_active"]), bool)

            # Last login should be datetime
            assert ti.infer_type(user["last_login"]) == DataType.DATETIME
            assert isinstance(ti.convert_value(user["last_login"]), datetime)

    def test_data_quality_analysis_scenario(self):
        """Test data quality analysis scenario."""
        ti = TypeInference()

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
            "25:00:00",    # Invalid time (hour > 24)
        ]

        # Analyze data quality
        type_counts = {}
        for value in messy_data:
            data_type = ti.infer_type(value)
            type_counts[data_type] = type_counts.get(data_type, 0) + 1

        # Check type distribution
        assert type_counts.get(DataType.INTEGER, 0) == 2  # "123", "  456  "
        assert type_counts.get(DataType.FLOAT, 0) == 1    # "789.12"
        assert type_counts.get(DataType.STRING, 0) == 3   # "abc", "not-a-date", "25:00:00"
        assert type_counts.get(DataType.EMPTY, 0) == 2    # "", "   "
        assert type_counts.get(DataType.BOOLEAN, 0) == 1  # "true"
        assert type_counts.get(DataType.DATE, 0) == 1     # "2023-01-01"

        # Invalid time should be string
        assert ti.infer_type("25:00:00") == DataType.STRING

    def test_batch_processing_scenario(self):
        """Test batch processing of large datasets."""
        ti = TypeInference()

        # Generate large dataset
        batch_size = 1000

        # Integer batch
        int_batch = [str(i) for i in range(batch_size)]
        int_profile = ti.profile_values(int_batch)
        assert int_profile == DataType.INTEGER

        # Float batch
        float_batch = [f"{i}.{i}" for i in range(batch_size)]
        float_profile = ti.profile_values(float_batch)
        assert float_profile == DataType.FLOAT

        # Mixed batch (integers + floats should return FLOAT)
        mixed_batch = int_batch[:500] + float_batch[:500]
        mixed_profile = ti.profile_values(mixed_batch)
        assert mixed_profile == DataType.FLOAT

        # Performance check - should handle large batches efficiently
        large_batch = [str(i) for i in range(5000)]
        large_profile = ti.profile_values(large_batch)
        assert large_profile == DataType.INTEGER

    def test_configuration_and_customization_scenario(self):
        """Test library usage with different configurations."""
        # Test different instance configurations
        ti1 = TypeInference()
        ti2 = TypeInference()

        # Both should behave identically
        test_value = "123"
        assert ti1.infer_type(test_value) == ti2.infer_type(test_value)
        assert ti1.convert_value(test_value) == ti2.convert_value(test_value)

        # Test threshold access
        threshold = TypeInference.get_incremental_typecheck_threshold()
        assert isinstance(threshold, int)
        assert threshold == ti1.get_incremental_typecheck_threshold()

    def test_error_handling_and_robustness_scenario(self):
        """Test error handling and robustness."""
        ti = TypeInference()

        # Test with None values
        assert ti.infer_type(None) == DataType.NONE  # None values are classified as NONE

        # Test with non-string types
        assert ti.infer_type(123) == DataType.INTEGER
        assert ti.infer_type(45.67) == DataType.FLOAT
        assert ti.infer_type(True) == DataType.BOOLEAN

        # Test conversion of edge cases
        assert ti.convert_value(None) is None  # None values remain None
        assert ti.convert_value(123) == 123  # Integers remain integers
        assert ti.convert_value(True) is True  # Booleans remain booleans

        # Test empty collections
        assert ti.profile_values([]) == DataType.EMPTY  # Empty collections return EMPTY

        # Test collections with None values
        mixed_with_none = ["123", None, "hello"]
        profile = ti.profile_values(mixed_with_none)
        assert profile == DataType.MIXED  # Should handle mixed types
