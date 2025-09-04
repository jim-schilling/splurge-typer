"""
splurge-typer - Type Inference and Conversion Library

This package provides comprehensive utilities for inferring Python data types from string values
and converting between different data representations.

Main Features:
- Single value type inference from strings
- Collection type analysis for determining dominant types
- Automatic type conversion with proper error handling
- Support for all major Python types including dates, times, and datetimes
- Performance optimizations for large datasets

Example Usage:
    >>> from splurge_typer import TypeInference, DataType
    >>>
    >>> # Single value inference
    >>> ti = TypeInference()
    >>> ti.infer_type('123')
    DataType.INTEGER
    >>>
    >>> # Collection analysis
    >>> ti.profile_values(['1', '2', '3'])
    DataType.INTEGER
    >>>
    >>> # Type conversion
    >>> ti.convert_value('123')
    123

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from .data_type import DataType
from .duck_typing import DuckTyping
from .string import String
from .type_inference import TypeInference

__version__ = "2025.0.0"
__all__ = ["DataType", "String", "TypeInference", "DuckTyping"]
