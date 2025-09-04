"""
Integration tests for splurge-typer library.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from datetime import date, datetime, time

from splurge_typer import DataType, String, TypeInference


class TestLibraryIntegration:
    """Integration tests for the complete library functionality."""

    def test_full_workflow_single_value(self):
        """Test complete workflow for single value processing."""
        ti = TypeInference()

        # Test integer
        value = "123"
        inferred_type = ti.infer_type(value)
        assert inferred_type == DataType.INTEGER

        converted = ti.convert_value(value)
        assert converted == 123
        assert isinstance(converted, int)

    def test_full_workflow_collection(self):
        """Test complete workflow for collection processing."""
        ti = TypeInference()

        # Test collection of integers
        values = ["1", "2", "3", "4", "5"]
        profile = ti.profile_values(values)
        assert profile == DataType.INTEGER

        # Convert all values
        converted_values = [ti.convert_value(v) for v in values]
        assert converted_values == [1, 2, 3, 4, 5]
        assert all(isinstance(v, int) for v in converted_values)

    def test_mixed_data_processing(self):
        """Test processing mixed data types."""
        ti = TypeInference()

        # Mixed collection
        mixed_values = ["123", "45.67", "true", "2023-01-01", "hello"]
        profile = ti.profile_values(mixed_values)
        assert profile == DataType.MIXED

        # Individual processing
        types = [ti.infer_type(v) for v in mixed_values]
        expected_types = [
            DataType.INTEGER,
            DataType.FLOAT,
            DataType.BOOLEAN,
            DataType.DATE,
            DataType.STRING
        ]
        assert types == expected_types

    def test_date_time_processing(self):
        """Test date and time processing integration."""
        ti = TypeInference()

        # Date processing
        date_str = "2023-12-25"
        assert ti.infer_type(date_str) == DataType.DATE
        converted_date = ti.convert_value(date_str)
        assert isinstance(converted_date, date)
        assert converted_date == date(2023, 12, 25)

        # Time processing
        time_str = "15:30:45"
        assert ti.infer_type(time_str) == DataType.TIME
        converted_time = ti.convert_value(time_str)
        assert isinstance(converted_time, time)
        assert converted_time == time(15, 30, 45)

        # Datetime processing
        datetime_str = "2023-12-25T15:30:45"
        assert ti.infer_type(datetime_str) == DataType.DATETIME
        converted_datetime = ti.convert_value(datetime_str)
        assert isinstance(converted_datetime, datetime)
        assert converted_datetime == datetime(2023, 12, 25, 15, 30, 45)

    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        ti = TypeInference()

        # Empty and whitespace
        assert ti.infer_type("") == DataType.EMPTY
        assert ti.convert_value("") == ""

        assert ti.infer_type("   ") == DataType.EMPTY
        assert ti.convert_value("   ") == ""

        # None values
        assert ti.infer_type("none") == DataType.NONE
        assert ti.convert_value("none") is None

        assert ti.infer_type("null") == DataType.NONE
        assert ti.convert_value("null") is None

    def test_large_dataset_performance(self):
        """Test performance with large datasets."""
        ti = TypeInference()

        # Create a large dataset of integers
        large_dataset = [str(i) for i in range(10000)]

        # Should handle large datasets efficiently
        profile = ti.profile_values(large_dataset)
        assert profile == DataType.INTEGER

        # Convert a sample to verify correctness
        sample_conversions = [ti.convert_value(v) for v in large_dataset[:10]]
        expected = list(range(10))
        assert sample_conversions == expected

    def test_string_utilities_integration(self):
        """Test integration between String utilities and TypeInference."""
        # Test that String utilities work with TypeInference results
        test_values = [
            ("123", DataType.INTEGER, 123),
            ("45.67", DataType.FLOAT, 45.67),
            ("true", DataType.BOOLEAN, True),
            ("hello", DataType.STRING, "hello"),
        ]

        for value_str, expected_type, expected_value in test_values:
            # String utility inference
            string_type = String.infer_type(value_str)
            assert string_type == expected_type

            # TypeInference result
            ti = TypeInference()
            ti_type = ti.infer_type(value_str)
            assert ti_type == expected_type

            # Conversion consistency
            ti_converted = ti.convert_value(value_str)
            assert ti_converted == expected_value

    def test_boolean_variations(self):
        """Test various boolean representations."""
        ti = TypeInference()

        true_variations = ["true", "True", "TRUE", "yes", "Yes", "YES"]
        false_variations = ["false", "False", "FALSE", "no", "No", "NO"]

        for variation in true_variations:
            assert ti.infer_type(variation) == DataType.BOOLEAN
            assert ti.convert_value(variation) is True

        for variation in false_variations:
            assert ti.infer_type(variation) == DataType.BOOLEAN
            assert ti.convert_value(variation) is False

    def test_numeric_edge_cases(self):
        """Test numeric edge cases."""
        ti = TypeInference()

        # Leading zeros
        assert ti.infer_type("00123") == DataType.INTEGER
        assert ti.convert_value("00123") == 123

        assert ti.infer_type("00123.4500") == DataType.FLOAT
        assert ti.convert_value("00123.4500") == 123.45

        # Scientific notation (should be treated as string)
        assert ti.infer_type("1.23e10") == DataType.STRING
        assert ti.convert_value("1.23e10") == "1.23e10"
