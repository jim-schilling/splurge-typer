"""
type_helper module - Provides utilities for type checking, conversion and inference

This module offers a comprehensive set of tools for:
- Type inference and validation
- Data type conversion
- String parsing and validation
- Collection type checking
- Value profiling and analysis

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from collections.abc import Iterable
from typing import Any

from splurge_typer.data_type import DataType
from splurge_typer.duck_typing import DuckTyping
from splurge_typer.string import String


class TypeInference:
    """
    TypeInference class - Provides methods for inferring data types and converting values to their inferred types.
    """

    _INCREMENTAL_TYPECHECK_THRESHOLD = 10_000

    @classmethod
    def get_incremental_typecheck_threshold(cls) -> int:
        """
        Get the incremental typecheck threshold.
        """
        return cls._INCREMENTAL_TYPECHECK_THRESHOLD

    @staticmethod
    def can_infer(
        value: Any,
    ) -> bool:
        """
        Check if the value can be inferred as a specific type.

        Args:
            value: The value to check

        Returns:
            True if the value can be inferred as a specific type, False otherwise
        """
        if not isinstance(value, str):
            return False

        inferred_type = String.infer_type(value)
        return inferred_type != DataType.STRING

    @staticmethod
    def infer_type(
        value: str,
    ) -> DataType:
        """
        Infer the type of the given value.

        Args:
            value: The value to infer the type for

        Returns:
            The inferred DataType
        """
        return String.infer_type(value)

    @classmethod
    def convert_value(
        cls,
        value: Any,
    ) -> Any:
        """
        Convert the value to its inferred type.

        Args:
            value: The value to convert

        Returns:
            The converted value in its inferred type
        """
        inferred_type = cls.infer_type(value)

        if inferred_type == DataType.BOOLEAN:
            return String.to_bool(value)
        if inferred_type == DataType.INTEGER:
            return String.to_int(value)
        if inferred_type == DataType.FLOAT:
            return String.to_float(value)
        if inferred_type == DataType.DATE:
            return String.to_date(value)
        if inferred_type == DataType.TIME:
            return String.to_time(value)
        if inferred_type == DataType.DATETIME:
            return String.to_datetime(value)
        if inferred_type == DataType.NONE:
            return None
        if inferred_type == DataType.EMPTY:
            return ""
        return value


    @staticmethod
    def _determine_type_from_counts(
        types: dict[str, int],
        count: int,
        *,
        allow_special_cases: bool = True,
    ) -> DataType | None:
        """
        Determine the data type based on type counts.

        Args:
            types: Dictionary of type counts
            count: Total number of values processed
            allow_special_cases: Whether to apply special case logic (all-digit strings, etc.)

        Returns:
            DataType if a definitive type can be determined, None otherwise
        """
        if types[DataType.EMPTY.name] == count:
            return DataType.EMPTY

        if types[DataType.NONE.name] == count:
            return DataType.NONE

        if types[DataType.NONE.name] + types[DataType.EMPTY.name] == count:
            return DataType.NONE

        if types[DataType.BOOLEAN.name] + types[DataType.EMPTY.name] == count:
            return DataType.BOOLEAN

        if types[DataType.STRING.name] + types[DataType.EMPTY.name] == count:
            return DataType.STRING

        # For early termination, skip complex logic that requires full analysis
        if not allow_special_cases:
            return None

        if types[DataType.DATE.name] + types[DataType.EMPTY.name] == count:
            return DataType.DATE

        if types[DataType.DATETIME.name] + types[DataType.EMPTY.name] == count:
            return DataType.DATETIME

        if types[DataType.TIME.name] + types[DataType.EMPTY.name] == count:
            return DataType.TIME

        if types[DataType.INTEGER.name] + types[DataType.EMPTY.name] == count:
            return DataType.INTEGER

        if types[DataType.FLOAT.name] + types[DataType.INTEGER.name] + types[DataType.EMPTY.name] == count:
            return DataType.FLOAT

        return None

    @classmethod
    def profile_values(
        cls,
        values: Iterable[Any],
        *,
        trim: bool = True,
        use_incremental_typecheck: bool = True,
    ) -> DataType:
        """
        Infer the most appropriate data type for a collection of values.

        This function analyzes a collection of values and determines the most
        appropriate data type that can represent all values in the collection.
        For lists of more than _INCREMENTAL_TYPECHECK_THRESHOLD items, it uses weighted incremental checks
        to short-circuit early when enough information is available to determine
        the final data type. For lists of _INCREMENTAL_TYPECHECK_THRESHOLD or fewer items, incremental
        type checking is disabled and a single pass is used.

        Args:
            values: Collection of values to analyze
            trim: Whether to trim whitespace before checking
            use_incremental_typecheck: Whether to use incremental type checking for early termination.
                                    For lists of _INCREMENTAL_TYPECHECK_THRESHOLD or fewer items, this is always False.

        Returns:
            DataType enum value representing the inferred type

        Raises:
            ValueError: If values is not iterable

        Examples:
            >>> profile_values(['1', '2', '3'])           # DataType.INTEGER
            >>> profile_values(['1.1', '2.2', '3.3'])     # DataType.FLOAT
            >>> profile_values(['1', '2.2', 'abc'])       # DataType.MIXED
            >>> profile_values(['true', 'false'])         # DataType.BOOLEAN
            >>> profile_values(['1', '2', '3'], use_incremental_typecheck=False)  # Full analysis
        """
        if not DuckTyping.is_iterable_not_string(values):
            msg = "values must be iterable"
            raise ValueError(msg)

        # Convert to list to handle generators and ensure we can iterate multiple times
        values_list: list[Any] = list(values)

        if not values_list:
            return DataType.EMPTY

        # Only enable incremental type checking for lists larger than the threshold
        if len(values_list) <= cls.get_incremental_typecheck_threshold():
            use_incremental_typecheck = False

        # Sequential processing with incremental checks
        types = {
            DataType.BOOLEAN.name: 0,
            DataType.DATE.name: 0,
            DataType.TIME.name: 0,
            DataType.DATETIME.name: 0,
            DataType.INTEGER.name: 0,
            DataType.FLOAT.name: 0,
            DataType.STRING.name: 0,
            DataType.EMPTY.name: 0,
            DataType.NONE.name: 0,
        }

        count = 0
        total_count = len(values_list)

        # Check points for early termination (25%, 50%, 75%) - only used if incremental checking is enabled
        check_points = {}
        if use_incremental_typecheck:
            check_points = {
                int(total_count * 0.25): False,
                int(total_count * 0.50): False,
                int(total_count * 0.75): False,
            }

        # First pass: count types with incremental checks
        for value in values_list:
            inferred_type = String.infer_type(value, trim=trim)
            types[inferred_type.name] += 1
            count += 1

            # Check for early termination at check points (only if incremental checking is enabled)
            if use_incremental_typecheck and count in check_points:
                # Only do early termination for very clear cases that don't involve
                # the special all-digit string logic or mixed int/float detection

                # Early detection of MIXED type: if we have both numeric/temporal types AND string types
                numeric_temporal_count = (
                    types[DataType.INTEGER.name]
                    + types[DataType.FLOAT.name]
                    + types[DataType.DATE.name]
                    + types[DataType.DATETIME.name]
                    + types[DataType.TIME.name]
                )
                string_count = types[DataType.STRING.name]

                if numeric_temporal_count > 0 and string_count > 0:
                    return DataType.MIXED

                early_result = cls._determine_type_from_counts(types, count, allow_special_cases=False)
                if early_result is not None:
                    return early_result

        # Final determination based on complete analysis
        final_result = cls._determine_type_from_counts(types, count, allow_special_cases=True)
        if final_result is not None:
            return final_result

        # Special case: if we have mixed DATE, TIME, DATETIME, INTEGER types,
        # check if all values are all-digit strings and prioritize INTEGER
        if types[DataType.DATE.name] + types[DataType.TIME.name] + types[DataType.DATETIME.name] + types[
            DataType.INTEGER.name
        ] + types[DataType.EMPTY.name] == count and (
            types[DataType.DATE.name] > 0
            or types[DataType.TIME.name] > 0
            or types[DataType.DATETIME.name] > 0
            or types[DataType.EMPTY.name] > 0
        ):
            # Second pass: check if all non-empty values are all-digit strings (with optional +/- signs)
            all_digit_values = True
            for value in values_list:
                if not String.is_empty_like(value, trim=trim) and not String.is_int_like(value, trim=trim):
                    all_digit_values = False
                    break

            if all_digit_values:
                return DataType.INTEGER

        return DataType.MIXED

    @staticmethod
    def is_list_like(value: Any) -> bool:
        """
        Check if value behaves like a list (duck typing).

        This method performs duck typing to determine if a value has list-like behavior,
        checking for the presence of common list methods.

        Args:
            value: Value to check for list-like behavior

        Returns:
            True if value is a list or has list-like behavior (append, remove, index methods)

        Examples:
            >>> TypeInference.is_list_like([1, 2, 3])        # True
            >>> TypeInference.is_list_like((1, 2, 3))        # False
            >>> TypeInference.is_list_like('abc')            # False
            >>> from collections import deque
            >>> TypeInference.is_list_like(deque([1, 2, 3])) # True
        """
        return DuckTyping.is_list_like(value)

    @staticmethod
    def is_dict_like(value: Any) -> bool:
        """
        Check if value behaves like a dictionary (duck typing).

        This method performs duck typing to determine if a value has dictionary-like behavior,
        checking for the presence of common dictionary methods.

        Args:
            value: Value to check for dictionary-like behavior

        Returns:
            True if value is a dict or has dict-like behavior (keys, get, values methods)

        Examples:
            >>> TypeInference.is_dict_like({'a': 1})         # True
            >>> TypeInference.is_dict_like([1, 2, 3])        # False
            >>> TypeInference.is_dict_like('abc')            # False
            >>> from collections import OrderedDict
            >>> TypeInference.is_dict_like(OrderedDict([('a', 1)])) # True
        """
        return DuckTyping.is_dict_like(value)

    @staticmethod
    def is_iterable(value: Any) -> bool:
        """
        Check if value is iterable.

        This method determines if a value supports iteration, either through the
        Iterable protocol or by having common iteration-related methods.

        Args:
            value: Value to check for iterability

        Returns:
            True if value is iterable (supports iteration)

        Examples:
            >>> TypeInference.is_iterable([1, 2, 3])         # True
            >>> TypeInference.is_iterable((1, 2, 3))         # True
            >>> TypeInference.is_iterable('abc')             # True
            >>> TypeInference.is_iterable(123)               # False
            >>> TypeInference.is_iterable({'a': 1})          # True
        """
        return DuckTyping.is_iterable(value)

    @staticmethod
    def is_iterable_not_string(value: Any) -> bool:
        """
        Check if value is iterable but not a string.

        This is useful for distinguishing between collections (lists, tuples, sets, etc.)
        and string values, which are also iterable but often need different handling.

        Args:
            value: Value to check

        Returns:
            True if value is iterable and not a string

        Examples:
            >>> TypeInference.is_iterable_not_string([1, 2, 3])  # True
            >>> TypeInference.is_iterable_not_string((1, 2, 3))  # True
            >>> TypeInference.is_iterable_not_string({'a': 1})   # True
            >>> TypeInference.is_iterable_not_string('abc')      # False
            >>> TypeInference.is_iterable_not_string(123)        # False
        """
        return DuckTyping.is_iterable_not_string(value)

    @staticmethod
    def is_empty(value: Any) -> bool:
        """
        Check if value is empty (None, empty string, or empty collection).

        This method provides a unified way to check for emptiness across different
        types of values, handling None, strings, and collections consistently.

        Args:
            value: Value to check for emptiness

        Returns:
            True if value is None, empty string, or empty collection

        Examples:
            >>> TypeInference.is_empty(None)           # True
            >>> TypeInference.is_empty('')             # True
            >>> TypeInference.is_empty('   ')          # True (whitespace-only)
            >>> TypeInference.is_empty([])             # True
            >>> TypeInference.is_empty({})             # True
            >>> TypeInference.is_empty(set())          # True
            >>> TypeInference.is_empty('abc')          # False
            >>> TypeInference.is_empty([1, 2, 3])      # False
        """
        return DuckTyping.is_empty(value)


