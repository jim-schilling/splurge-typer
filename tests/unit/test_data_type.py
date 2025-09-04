"""
Unit tests for DataType enum.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""


from splurge_typer.data_type import DataType


class TestDataType:
    """Test cases for DataType enum functionality."""

    def test_data_type_values(self):
        """Test that DataType enum has expected string values."""
        assert DataType.STRING.value == "str"
        assert DataType.INTEGER.value == "int"
        assert DataType.FLOAT.value == "float"
        assert DataType.BOOLEAN.value == "bool"
        assert DataType.DATE.value == "date"
        assert DataType.TIME.value == "time"
        assert DataType.DATETIME.value == "datetime"
        assert DataType.MIXED.value == "mixed"
        assert DataType.EMPTY.value == "empty"
        assert DataType.NONE.value == "none"

    def test_data_type_enum_members(self):
        """Test that all expected enum members exist."""
        expected_members = {
            "STRING", "INTEGER", "FLOAT", "BOOLEAN", "DATE", "TIME",
            "DATETIME", "MIXED", "EMPTY", "NONE"
        }
        actual_members = {member.name for member in DataType}
        assert actual_members == expected_members

    def test_data_type_string_representation(self):
        """Test string representation of DataType enum."""
        assert str(DataType.INTEGER) == "DataType.INTEGER"
        assert repr(DataType.INTEGER) == "<DataType.INTEGER: 'int'>"

    def test_data_type_equality(self):
        """Test equality comparisons between DataType values."""
        assert DataType.INTEGER == DataType.INTEGER
        assert DataType.STRING != DataType.INTEGER
        assert DataType.INTEGER != "int"  # Different types

    def test_data_type_hashable(self):
        """Test that DataType values can be used as dictionary keys."""
        type_dict = {DataType.INTEGER: "number", DataType.STRING: "text"}
        assert type_dict[DataType.INTEGER] == "number"
        assert type_dict[DataType.STRING] == "text"

    def test_data_type_iteration(self):
        """Test that DataType can be iterated over."""
        types = list(DataType)
        assert len(types) == 10
        assert DataType.STRING in types
        assert DataType.INTEGER in types
