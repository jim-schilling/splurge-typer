"""
data_type module - Provides enumeration of supported data types

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from enum import Enum


class DataType(Enum):
    """
    Enumeration of supported data types for type inference and conversion.

    This enum defines the core data types that can be inferred and converted:
    - STRING: Text data
    - INTEGER: Whole numbers
    - FLOAT: Decimal numbers
    - BOOLEAN: True/False values
    - DATE: Calendar dates
    - TIME: Time values
    - DATETIME: Combined date and time
    - MIXED: Multiple types in collection
    - EMPTY: Empty values
    - NONE: Null/None values
    """

    STRING = "str"
    INTEGER = "int"
    FLOAT = "float"
    BOOLEAN = "bool"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    MIXED = "mixed"
    EMPTY = "empty"
    NONE = "none"
