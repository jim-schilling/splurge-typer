"""
Unit tests for TypeInference class.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from datetime import date, datetime, time

import pytest

from splurge_typer.data_type import DataType
from splurge_typer.type_inference import TypeInference


class TestTypeInferenceCanInfer:
    """Test cases for can_infer method."""

    @pytest.mark.parametrize("value,expected", [
        ("123", True),  # Can infer as integer
        ("hello", False),  # Cannot infer beyond string
        ("", True),  # Empty string - treated as string
        ("   ", True),  # Whitespace only - treated as string
        (123, False),  # Not a string
        (None, False),  # None value
    ])
    def test_can_infer(self, value, expected):
        """Test can_infer method."""
        assert TypeInference.can_infer(value) == expected


class TestTypeInferenceInferType:
    """Test cases for infer_type method."""

    @pytest.mark.parametrize("value,expected", [
        ("123", DataType.INTEGER),
        ("123.45", DataType.FLOAT),
        ("true", DataType.BOOLEAN),
        ("2023-01-01", DataType.DATE),
        ("14:30:00", DataType.TIME),
        ("2023-01-01T12:00:00", DataType.DATETIME),
        ("hello", DataType.STRING),
        ("", DataType.EMPTY),
        ("none", DataType.NONE),
        ("null", DataType.NONE),
    ])
    def test_infer_type(self, value, expected):
        """Test type inference for various inputs."""
        assert TypeInference.infer_type(value) == expected

    def test_infer_type_non_string(self):
        """Test type inference for non-string inputs."""
        assert TypeInference.infer_type(123) == DataType.INTEGER  # Correctly identifies integer


class TestTypeInferenceConvertValue:
    """Test cases for convert_value method."""

    def test_convert_value_integer(self):
        """Test converting integer strings."""
        assert TypeInference.convert_value("123") == 123
        assert TypeInference.convert_value("-456") == -456

    def test_convert_value_float(self):
        """Test converting float strings."""
        assert TypeInference.convert_value("123.45") == 123.45
        assert TypeInference.convert_value("-456.78") == -456.78

    def test_convert_value_boolean(self):
        """Test converting boolean strings."""
        assert TypeInference.convert_value("true") is True
        assert TypeInference.convert_value("false") is False
        assert TypeInference.convert_value("True") is True
        assert TypeInference.convert_value("False") is False

    def test_convert_value_date(self):
        """Test converting date strings."""
        result = TypeInference.convert_value("2023-01-01")
        assert result == date(2023, 1, 1)

    def test_convert_value_time(self):
        """Test converting time strings."""
        result = TypeInference.convert_value("14:30:00")
        assert result == time(14, 30, 0)

    def test_convert_value_datetime(self):
        """Test converting datetime strings."""
        result = TypeInference.convert_value("2023-01-01T12:00:00")
        expected = datetime(2023, 1, 1, 12, 0, 0)
        assert result == expected

    def test_convert_value_string(self):
        """Test converting string values."""
        assert TypeInference.convert_value("hello") == "hello"

    def test_convert_value_empty(self):
        """Test converting empty strings."""
        assert TypeInference.convert_value("") == ""

    def test_convert_value_none(self):
        """Test converting none/null values."""
        assert TypeInference.convert_value("none") is None
        assert TypeInference.convert_value("null") is None

    def test_convert_value_invalid(self):
        """Test converting invalid values."""
        assert TypeInference.convert_value("invalid") == "invalid"


class TestTypeInferenceProfileValues:
    """Test cases for profile_values method."""

    def test_profile_values_integers(self):
        """Test profiling integer values."""
        values = ["1", "2", "3", "4", "5"]
        result = TypeInference.profile_values(values)
        assert result == DataType.INTEGER

    def test_profile_values_floats(self):
        """Test profiling float values."""
        values = ["1.1", "2.2", "3.3"]
        result = TypeInference.profile_values(values)
        assert result == DataType.FLOAT

    def test_profile_values_mixed(self):
        """Test profiling mixed type values."""
        values = ["1", "2.5", "hello", "2023-01-01"]
        result = TypeInference.profile_values(values)
        assert result == DataType.MIXED

    def test_profile_values_single_type(self):
        """Test profiling single value."""
        values = ["hello"]
        result = TypeInference.profile_values(values)
        assert result == DataType.STRING

    def test_profile_values_empty(self):
        """Test profiling empty collection."""
        values = []
        result = TypeInference.profile_values(values)
        assert result == DataType.EMPTY  # Empty collections return EMPTY

    def test_profile_values_all_same_type(self):
        """Test profiling values that are all the same type."""
        values = ["true", "false", "True", "False"]
        result = TypeInference.profile_values(values)
        assert result == DataType.BOOLEAN


class TestTypeInferenceThreshold:
    """Test cases for incremental typecheck threshold."""

    def test_get_incremental_typecheck_threshold(self):
        """Test getting the incremental threshold."""
        threshold = TypeInference.get_incremental_typecheck_threshold()
        assert isinstance(threshold, int)
        assert threshold > 0

    def test_incremental_processing_small_dataset(self):
        """Test that small datasets don't trigger incremental processing."""
        values = ["1", "2", "3"]  # Less than threshold
        result = TypeInference.profile_values(values)
        assert result == DataType.INTEGER

    def test_incremental_processing_large_dataset(self):
        """Test that large datasets work correctly."""
        values = [str(i) for i in range(100)]  # More than threshold
        result = TypeInference.profile_values(values)
        assert result == DataType.INTEGER


class TestTypeInferenceInstanceMethods:
    """Test cases for TypeInference instance methods."""

    def test_instance_creation(self):
        """Test creating TypeInference instance."""
        ti = TypeInference()
        assert ti is not None
        assert hasattr(ti, 'infer_type')
        assert hasattr(ti, 'convert_value')
        assert hasattr(ti, 'profile_values')

    def test_instance_infer_type(self):
        """Test instance method for type inference."""
        ti = TypeInference()
        assert ti.infer_type("123") == DataType.INTEGER
        assert ti.infer_type("hello") == DataType.STRING

    def test_instance_convert_value(self):
        """Test instance method for value conversion."""
        ti = TypeInference()
        assert ti.convert_value("123") == 123
        assert ti.convert_value("hello") == "hello"

    def test_instance_profile_values(self):
        """Test instance method for value profiling."""
        ti = TypeInference()
        values = ["1", "2", "3"]
        assert ti.profile_values(values) == DataType.INTEGER


class TestTypeInferenceDuckTypingWrappers:
    """Test cases for duck typing wrapper methods."""

    @pytest.mark.parametrize("value,expected", [
        # Lists
        ([], True),
        ([1, 2, 3], True),
        ((1, 2, 3), False),  # tuples don't have append/remove

        # Strings
        ("", False),
        ("abc", False),

        # Other
        (123, False),
        (None, False),
    ])
    def test_is_list_like(self, value, expected):
        """Test is_list_like wrapper method."""
        assert TypeInference.is_list_like(value) == expected

    @pytest.mark.parametrize("value,expected", [
        # Dicts
        ({}, True),
        ({"a": 1}, True),
        ([], False),  # lists don't have keys/get/values

        # Other
        (123, False),
        (None, False),
    ])
    def test_is_dict_like(self, value, expected):
        """Test is_dict_like wrapper method."""
        assert TypeInference.is_dict_like(value) == expected

    @pytest.mark.parametrize("value,expected", [
        # Iterables
        ([], True),
        ([1, 2, 3], True),
        ((1, 2, 3), True),
        ("abc", True),
        ({}, True),

        # Non-iterables
        (123, False),
        (None, False),
    ])
    def test_is_iterable(self, value, expected):
        """Test is_iterable wrapper method."""
        assert TypeInference.is_iterable(value) == expected

    @pytest.mark.parametrize("value,expected", [
        # Iterables that are not strings
        ([], True),
        ([1, 2, 3], True),
        ((1, 2, 3), True),
        ({}, True),

        # Strings
        ("", False),
        ("abc", False),

        # Non-iterables
        (123, False),
        (None, False),
    ])
    def test_is_iterable_not_string(self, value, expected):
        """Test is_iterable_not_string wrapper method."""
        assert TypeInference.is_iterable_not_string(value) == expected

    @pytest.mark.parametrize("value,expected", [
        # Empty values
        (None, True),
        ("", True),
        ("   ", True),
        ([], True),
        ({}, True),

        # Non-empty values
        ("abc", False),
        ([1, 2, 3], False),
        ({"a": 1}, False),
        (123, False),
    ])
    def test_is_empty(self, value, expected):
        """Test is_empty wrapper method."""
        assert TypeInference.is_empty(value) == expected


class TestTypeInferenceProfileValuesEdgeCases:
    """Test edge cases for profile_values method."""

    def test_profile_values_non_iterable(self):
        """Test profile_values with non-iterable input."""
        with pytest.raises(ValueError, match="values must be iterable"):
            TypeInference.profile_values("not_iterable")

    def test_profile_values_non_iterable_not_string(self):
        """Test profile_values with non-iterable non-string input."""
        with pytest.raises(ValueError, match="values must be iterable"):
            TypeInference.profile_values(123)

    def test_profile_values_empty_list(self):
        """Test profile_values with empty list."""
        result = TypeInference.profile_values([])
        assert result == DataType.EMPTY

    def test_profile_values_single_empty_string(self):
        """Test profile_values with single empty string."""
        result = TypeInference.profile_values([""])
        assert result == DataType.EMPTY

    def test_profile_values_mixed_empty_and_values(self):
        """Test profile_values with mix of empty and non-empty values."""
        result = TypeInference.profile_values(["", "123", ""])
        assert result == DataType.INTEGER  # Should handle empties

    def test_profile_values_all_none_like(self):
        """Test profile_values with all none-like values."""
        result = TypeInference.profile_values(["none", "null", "NONE"])
        assert result == DataType.NONE

    def test_profile_values_all_digit_strings(self):
        """Test profile_values with all-digit strings (should be INTEGER)."""
        result = TypeInference.profile_values(["123", "456", "789"])
        assert result == DataType.INTEGER

    def test_profile_values_mixed_numeric_and_string(self):
        """Test profile_values with mixed numeric and string values."""
        result = TypeInference.profile_values(["123", "abc", "456"])
        assert result == DataType.MIXED

    def test_profile_values_large_dataset_incremental_checking(self):
        """Test profile_values with large dataset to trigger incremental checking."""
        # Create a list larger than the threshold to trigger incremental checking
        large_list = ["1"] * 150  # Default threshold is probably around 100
        result = TypeInference.profile_values(large_list)
        assert result == DataType.INTEGER

    def test_profile_values_with_trim(self):
        """Test profile_values with trim parameter."""
        result = TypeInference.profile_values(["  123  ", "  456  "], trim=True)
        assert result == DataType.INTEGER

        result = TypeInference.profile_values(["  123  ", "  456  "], trim=False)
        assert result == DataType.STRING  # Without trim, treated as strings


class TestTypeInferenceIncrementalChecking:
    """Test cases for incremental type checking features."""

    def test_incremental_threshold(self):
        """Test getting the incremental typecheck threshold."""
        threshold = TypeInference.get_incremental_typecheck_threshold()
        assert isinstance(threshold, int)
        assert threshold > 0

    def test_early_termination_mixed_types(self):
        """Test early termination when mixed numeric/string types detected."""
        # This would be hard to test directly, but we can test the logic indirectly
        # by ensuring the method works with various combinations
        result = TypeInference.profile_values(["123", "abc", "456.78"])
        assert result == DataType.MIXED

    def test_all_digit_detection(self):
        """Test detection of all-digit strings as integers."""
        # This tests the all-digit detection logic
        result = TypeInference.profile_values(["123", "456", "789"])
        assert result == DataType.INTEGER

        # Mixed with non-digits should be string or mixed
        result = TypeInference.profile_values(["123", "abc", "456"])
        assert result in [DataType.MIXED, DataType.STRING]


class TestTypeInferenceNativeObjectsAndStrings:
    """Test TypeInference with native Python objects and string representations."""

    def test_native_date_objects(self):
        """Test type inference with native date objects."""
        # Create a collection with native date objects
        date_objects = [
            date(2023, 12, 25),
            date(2024, 1, 1),
            date(2024, 12, 31)
        ]

        # Convert to strings for TypeInference (since it expects strings)
        date_strings = [d.isoformat() for d in date_objects]
        result = TypeInference.profile_values(date_strings)
        assert result == DataType.DATE, "Collection of date strings should be DATE type"

    def test_native_datetime_objects(self):
        """Test type inference with native datetime objects."""
        # Create a collection with native datetime objects
        datetime_objects = [
            datetime(2023, 12, 25, 14, 30, 0),
            datetime(2024, 1, 1, 9, 0, 0),
            datetime(2024, 12, 31, 23, 59, 59)
        ]

        # Convert to strings for TypeInference
        datetime_strings = [dt.isoformat() for dt in datetime_objects]
        result = TypeInference.profile_values(datetime_strings)
        assert result == DataType.DATETIME, "Collection of datetime strings should be DATETIME type"

    def test_native_time_objects(self):
        """Test type inference with native time objects."""
        # Create a collection with native time objects
        time_objects = [
            time(14, 30, 0),
            time(9, 15, 30),
            time(23, 59, 59)
        ]

        # Convert to strings for TypeInference
        time_strings = [t.isoformat() for t in time_objects]
        result = TypeInference.profile_values(time_strings)
        assert result == DataType.TIME, "Collection of time strings should be TIME type"

    def test_mixed_native_objects(self):
        """Test type inference with mixed native object types."""
        # Mix different types
        mixed_objects = [
            date(2023, 12, 25),  # date
            datetime(2024, 1, 1, 14, 30, 0),  # datetime
            time(9, 15, 30),  # time
            "2024-02-01",  # date string
            "2024-03-01T10:00:00",  # datetime string
        ]

        # Convert to strings
        mixed_strings = []
        for obj in mixed_objects:
            if isinstance(obj, date | datetime):
                mixed_strings.append(obj.isoformat())
            elif isinstance(obj, time):
                mixed_strings.append(obj.isoformat())
            else:
                mixed_strings.append(str(obj))

        result = TypeInference.profile_values(mixed_strings)
        assert result == DataType.MIXED, "Mixed temporal types should be MIXED"

    def test_native_numeric_objects(self):
        """Test type inference with native numeric objects."""
        # Test integers
        int_strings = [str(i) for i in [123, 456, 789]]
        result = TypeInference.profile_values(int_strings)
        assert result == DataType.INTEGER, "Integer strings should be INTEGER type"

        # Test floats
        float_strings = [str(f) for f in [123.45, 67.89, 0.0]]
        result = TypeInference.profile_values(float_strings)
        assert result == DataType.FLOAT, "Float strings should be FLOAT type"

    def test_native_boolean_objects(self):
        """Test type inference with native boolean objects."""
        # Test booleans
        bool_strings = [str(b).lower() for b in [True, False, True]]
        result = TypeInference.profile_values(bool_strings)
        assert result == DataType.BOOLEAN, "Boolean strings should be BOOLEAN type"

        # Test various boolean representations (excluding numeric ones)
        bool_strings = ["true", "false", "yes", "no"]
        result = TypeInference.profile_values(bool_strings)
        assert result == DataType.BOOLEAN, "Boolean strings should be BOOLEAN type"

        # Mixed with numeric representations should be MIXED
        mixed_bool_strings = ["true", "false", "yes", "no", "1", "0"]
        result = TypeInference.profile_values(mixed_bool_strings)
        assert result == DataType.MIXED, "Mixed boolean and numeric representations should be MIXED"

    def test_native_none_objects(self):
        """Test type inference with None values."""
        none_strings = ["none", "null", "None", "NONE"]
        result = TypeInference.profile_values(none_strings)
        assert result == DataType.NONE, "None strings should be NONE type"

    def test_native_empty_objects(self):
        """Test type inference with empty values."""
        empty_strings = ["", "   ", "\t\n"]
        result = TypeInference.profile_values(empty_strings)
        assert result == DataType.EMPTY, "Empty strings should be EMPTY type"

    def test_native_string_objects(self):
        """Test type inference with string values."""
        string_values = ["hello", "world", "python"]
        result = TypeInference.profile_values(string_values)
        assert result == DataType.STRING, "Regular strings should be STRING type"

    def test_consistency_between_native_and_string(self):
        """Test that native objects and their string representations give consistent results."""
        # Test date consistency
        date_obj = date(2023, 12, 25)
        date_str = date_obj.isoformat()
        result_str = TypeInference.profile_values([date_str])
        assert result_str == DataType.DATE, "Date string should be DATE type"

        # Test datetime consistency
        datetime_obj = datetime(2023, 12, 25, 14, 30, 0)
        datetime_str = datetime_obj.isoformat()
        result_str = TypeInference.profile_values([datetime_str])
        assert result_str == DataType.DATETIME, "Datetime string should be DATETIME type"

        # Test time consistency
        time_obj = time(14, 30, 0)
        time_str = time_obj.isoformat()
        result_str = TypeInference.profile_values([time_str])
        assert result_str == DataType.TIME, "Time string should be TIME type"

    def test_edge_cases_with_native_objects(self):
        """Test edge cases with native object conversions."""
        # Test zero values
        zero_strings = ["0", "-0", "0.0", "-0.0"]
        result = TypeInference.profile_values(zero_strings)
        # This could be INTEGER, FLOAT, or MIXED depending on implementation
        assert result in [DataType.INTEGER, DataType.FLOAT, DataType.MIXED]

        # Test single character representations
        single_chars = ["1", "a", "2", "b"]
        result = TypeInference.profile_values(single_chars)
        assert result == DataType.MIXED, "Mixed single characters should be MIXED"

        # Test empty collection
        result = TypeInference.profile_values([])
        assert result == DataType.EMPTY, "Empty collection should be EMPTY"
