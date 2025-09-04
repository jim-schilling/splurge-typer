"""
Unit tests for DuckTyping class.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from collections import OrderedDict, UserDict, UserList, deque

import pytest

from splurge_typer.duck_typing import DuckTyping


class TestDuckTypingIsListLike:
    """Test cases for is_list_like method."""

    @pytest.mark.parametrize("value,expected", [
        # Standard lists
        ([], True),
        ([1, 2, 3], True),
        (["a", "b", "c"], True),

        # Tuples - should be False (no append/remove methods)
        ((), False),
        ((1, 2, 3), False),

        # Strings - should be False
        ("", False),
        ("abc", False),

        # Sets - should be False (no index method)
        (set(), False),
        ({1, 2, 3}, False),

        # Dict - should be False
        ({}, False),
        ({"a": 1}, False),

        # deque - should be True (has append, remove, index)
        (deque(), True),
        (deque([1, 2, 3]), True),

        # UserList - should be True
        (UserList(), True),
        (UserList([1, 2, 3]), True),

        # None - should be False
        (None, False),

        # Numbers - should be False
        (123, False),
        (123.45, False),
    ])
    def test_is_list_like(self, value, expected):
        """Test is_list_like method with various inputs."""
        assert DuckTyping.is_list_like(value) == expected


class TestDuckTypingIsDictLike:
    """Test cases for is_dict_like method."""

    @pytest.mark.parametrize("value,expected", [
        # Standard dicts
        ({}, True),
        ({"a": 1}, True),
        ({"key": "value"}, True),

        # Lists - should be False
        ([], False),
        ([1, 2, 3], False),

        # Tuples - should be False
        ((), False),
        ((1, 2), False),

        # Strings - should be False
        ("", False),
        ("abc", False),

        # Sets - should be False
        (set(), False),
        ({1, 2, 3}, False),

        # OrderedDict - should be True
        (OrderedDict(), True),
        (OrderedDict([("a", 1)]), True),

        # UserDict - should be True
        (UserDict(), True),
        (UserDict({"a": 1}), True),

        # None - should be False
        (None, False),

        # Numbers - should be False
        (123, False),
        (123.45, False),
    ])
    def test_is_dict_like(self, value, expected):
        """Test is_dict_like method with various inputs."""
        assert DuckTyping.is_dict_like(value) == expected


class TestDuckTypingIsIterable:
    """Test cases for is_iterable method."""

    @pytest.mark.parametrize("value,expected", [
        # Lists
        ([], True),
        ([1, 2, 3], True),

        # Tuples
        ((), True),
        ((1, 2, 3), True),

        # Strings
        ("", True),
        ("abc", True),

        # Sets
        (set(), True),
        ({1, 2, 3}, True),

        # Dicts
        ({}, True),
        ({"a": 1}, True),

        # Generators
        ((x for x in range(3)), True),

        # Range
        (range(5), True),

        # None - should be False
        (None, False),

        # Numbers - should be False
        (123, False),
        (123.45, False),
    ])
    def test_is_iterable(self, value, expected):
        """Test is_iterable method with various inputs."""
        assert DuckTyping.is_iterable(value) == expected


class TestDuckTypingIsIterableNotString:
    """Test cases for is_iterable_not_string method."""

    @pytest.mark.parametrize("value,expected", [
        # Lists - should be True
        ([], True),
        ([1, 2, 3], True),

        # Tuples - should be True
        ((), True),
        ((1, 2, 3), True),

        # Sets - should be True
        (set(), True),
        ({1, 2, 3}, True),

        # Dicts - should be True
        ({}, True),
        ({"a": 1}, True),

        # Strings - should be False
        ("", False),
        ("abc", False),

        # None - should be False
        (None, False),

        # Numbers - should be False
        (123, False),
        (123.45, False),
    ])
    def test_is_iterable_not_string(self, value, expected):
        """Test is_iterable_not_string method with various inputs."""
        assert DuckTyping.is_iterable_not_string(value) == expected


class TestDuckTypingIsEmpty:
    """Test cases for is_empty method."""

    @pytest.mark.parametrize("value,expected", [
        # None
        (None, True),

        # Empty strings
        ("", True),
        ("   ", True),  # whitespace only
        ("\t\n", True),  # tabs and newlines

        # Non-empty strings
        ("abc", False),
        ("   abc   ", False),

        # Empty collections
        ([], True),
        ({}, True),
        (set(), True),
        ((), True),
        (deque(), True),

        # Non-empty collections
        ([1, 2, 3], False),
        ({"a": 1}, False),
        ({1, 2, 3}, False),
        ((1, 2), False),

        # Numbers - should be False (not empty)
        (0, False),
        (123, False),
        (123.45, False),

        # Booleans - should be False (not empty)
        (True, False),
        (False, False),
    ])
    def test_is_empty(self, value, expected):
        """Test is_empty method with various inputs."""
        assert DuckTyping.is_empty(value) == expected


class TestDuckTypingGetBehaviorType:
    """Test cases for get_behavior_type method."""

    @pytest.mark.parametrize("value,expected", [
        # Empty values
        (None, "empty"),
        ("", "empty"),
        ("   ", "empty"),
        ([], "empty"),
        ({}, "empty"),

        # Strings
        ("abc", "string"),
        ("hello world", "string"),

        # List-like
        ([1, 2, 3], "list-like"),
        (deque([1, 2, 3]), "list-like"),

        # Dict-like
        ({"a": 1}, "dict-like"),
        (OrderedDict([("a", 1)]), "dict-like"),

        # Other iterables (not list-like or dict-like)
        ((1, 2, 3), "iterable"),
        ({1, 2, 3}, "iterable"),
        (range(5), "iterable"),

        # Scalars
        (123, "scalar"),
        (123.45, "scalar"),
        (True, "scalar"),
        (False, "scalar"),
    ])
    def test_get_behavior_type(self, value, expected):
        """Test get_behavior_type method with various inputs."""
        assert DuckTyping.get_behavior_type(value) == expected


class TestDuckTypingEdgeCases:
    """Test edge cases and special scenarios."""

    def test_custom_objects_with_list_behavior(self):
        """Test custom objects that implement list-like behavior."""

        class CustomList:
            def __init__(self, items=None):
                self.items = items or []

            def __iter__(self):
                return iter(self.items)

            def append(self, item):
                self.items.append(item)

            def remove(self, item):
                self.items.remove(item)

            def index(self, item):
                return self.items.index(item)

        custom_list = CustomList([1, 2, 3])
        assert DuckTyping.is_list_like(custom_list) is True
        assert DuckTyping.get_behavior_type(custom_list) == "list-like"

    def test_custom_objects_with_dict_behavior(self):
        """Test custom objects that implement dict-like behavior."""

        class CustomDict:
            def __init__(self, data=None):
                self.data = data or {}

            def keys(self):
                return self.data.keys()

            def get(self, key, default=None):
                return self.data.get(key, default)

            def values(self):
                return self.data.values()

        custom_dict = CustomDict({"a": 1, "b": 2})
        assert DuckTyping.is_dict_like(custom_dict) is True
        assert DuckTyping.get_behavior_type(custom_dict) == "dict-like"

    def test_objects_without_len_method(self):
        """Test objects without __len__ method for emptiness."""

        class NoLenMethod:
            def __init__(self, value):
                self.value = value

        obj = NoLenMethod("test")
        assert DuckTyping.is_empty(obj) is False  # No __len__, so not empty

    def test_iterable_objects_with_exceptions(self):
        """Test objects that raise TypeError during iteration."""

        class BrokenIterable:
            def __iter__(self):
                raise TypeError("Cannot iterate")

        broken = BrokenIterable()
        # Should be considered iterable since it has __iter__ (fallback check)
        assert DuckTyping.is_iterable(broken) is True

    def test_non_iterable_custom_objects(self):
        """Test custom objects that are not iterable."""

        class NonIterable:
            def __init__(self, value):
                self.value = value

        non_iterable = NonIterable(42)
        assert DuckTyping.is_iterable(non_iterable) is False
        assert DuckTyping.is_iterable_not_string(non_iterable) is False
        assert DuckTyping.get_behavior_type(non_iterable) == "scalar"
