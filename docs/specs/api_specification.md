# splurge-typer API Specification

## Overview

This document specifies the complete Application Programming Interface (API) for the **splurge-typer** library, including all public classes, methods, parameters, return types, and usage patterns.

## API Architecture

### Core Components

The API consists of four main components:

1. **TypeInference Class**: Main interface for type inference and conversion operations
2. **String Class**: Low-level string processing utilities
3. **DuckTyping Class**: Duck typing utilities for behavioral type checking
4. **DataType Enum**: Enumeration of supported data types

### Import Structure

```python
# Recommended import pattern
from splurge_typer import TypeInference, DataType, String, DuckTyping

# Alternative imports
from splurge_typer import TypeInference as TI
from splurge_typer.data_type import DataType
from splurge_typer.string import String
from splurge_typer.duck_typing import DuckTyping
```

## TypeInference Class

### Class Description
The `TypeInference` class provides the main interface for type inference and conversion operations. It supports both instance methods for common operations and static methods for utility functions.

**Note:** For backward compatibility, duck typing utility methods are still available in this class but delegate to the `DuckTyping` class for the actual implementation. For new code, consider using `DuckTyping` directly for better modularity.

### Constructor

#### `TypeInference()`
Creates a new TypeInference instance.

**Parameters:** None

**Returns:** TypeInference instance

**Example:**
```python
ti = TypeInference()
```

### Instance Methods

#### `infer_type(value: str) -> DataType`
Infer the data type of a string value.

**Parameters:**
- `value` (str): The string value to analyze

**Returns:**
- `DataType`: The inferred data type

**Raises:** None (graceful error handling)

**Example:**
```python
result = ti.infer_type("123")
# Returns: DataType.INTEGER

result = ti.infer_type("2023-01-01")
# Returns: DataType.DATE
```

#### `convert_value(value: Any) -> Any`
Convert a value to its inferred Python type.

**Parameters:**
- `value` (Any): The value to convert (typically a string)

**Returns:**
- `Any`: The converted value in its appropriate Python type

**Raises:** None (graceful error handling)

**Type Conversions:**
- `"123"` → `123` (int)
- `"123.45"` → `123.45` (float)
- `"true"` → `True` (bool)
- `"2023-01-01"` → `datetime.date(2023, 1, 1)`
- `"14:30:00"` → `datetime.time(14, 30, 0)`
- `"2023-01-01T12:00:00"` → `datetime.datetime(2023, 1, 1, 12, 0, 0)` (ISO format)
- `"2023-01-01 12:00:00"` → `datetime.datetime(2023, 1, 1, 12, 0, 0)` (space separated)
- `"hello"` → `"hello"` (str, unchanged)
- `""` → `""` (str, unchanged)
- `"none"` → `None`

**Example:**
```python
result = ti.convert_value("123")
# Returns: 123 (integer)

result = ti.convert_value("true")
# Returns: True (boolean)
```

#### `profile_values(values: Iterable[Any]) -> DataType`
Analyze a collection of values to determine the dominant type.

**Parameters:**
- `values` (Iterable[Any]): Collection of values to analyze

**Returns:**
- `DataType`: The dominant data type in the collection

**Behavior:**
- For homogeneous collections: Returns the common type
- For heterogeneous collections: Returns `DataType.MIXED`
- For empty collections: Returns `DataType.MIXED`
- Automatically uses incremental processing for large datasets (>10,000 items)

**Example:**
```python
result = ti.profile_values(["1", "2", "3"])
# Returns: DataType.INTEGER

result = ti.profile_values(["1", "hello", "true"])
# Returns: DataType.MIXED
```

### Static Methods

#### `TypeInference.can_infer(value: Any) -> bool`
Check if a value can be inferred as a specific type (not STRING).

**Parameters:**
- `value` (Any): The value to check

**Returns:**
- `bool`: True if the value can be inferred as a specific type, False otherwise

**Example:**
```python
result = TypeInference.can_infer("123")
# Returns: True

result = TypeInference.can_infer("hello")
# Returns: False (falls back to STRING)
```

#### `TypeInference.get_incremental_typecheck_threshold() -> int`
Get the threshold for incremental type checking.

**Parameters:** None

**Returns:**
- `int`: The current threshold value (default: 10,000)

**Example:**
```python
threshold = TypeInference.get_incremental_typecheck_threshold()
# Returns: 10000
```

#### `TypeInference.is_list_like(value: Any) -> bool`
Check if value behaves like a list (duck typing).

This method performs duck typing to determine if a value has list-like behavior,
checking for the presence of common list methods.

**Note:** This method delegates to `DuckTyping.is_list_like()` for backward compatibility.

**Parameters:**
- `value` (Any): Value to check for list-like behavior

**Returns:**
- `bool`: True if value is a list or has list-like behavior (append, remove, index methods)

**Example:**
```python
result = TypeInference.is_list_like([1, 2, 3])
# Returns: True

result = TypeInference.is_list_like((1, 2, 3))
# Returns: False

from collections import deque
result = TypeInference.is_list_like(deque([1, 2, 3]))
# Returns: True
```

#### `TypeInference.is_dict_like(value: Any) -> bool`
Check if value behaves like a dictionary (duck typing).

This method performs duck typing to determine if a value has dictionary-like behavior,
checking for the presence of common dictionary methods.

**Parameters:**
- `value` (Any): Value to check for dictionary-like behavior

**Returns:**
- `bool`: True if value is a dict or has dict-like behavior (keys, get, values methods)

**Example:**
```python
result = TypeInference.is_dict_like({'a': 1})
# Returns: True

result = TypeInference.is_dict_like([1, 2, 3])
# Returns: False

from collections import OrderedDict
result = TypeInference.is_dict_like(OrderedDict([('a', 1)]))
# Returns: True
```

#### `TypeInference.is_iterable(value: Any) -> bool`
Check if value is iterable.

This method determines if a value supports iteration, either through the
Iterable protocol or by having common iteration-related methods.

**Parameters:**
- `value` (Any): Value to check for iterability

**Returns:**
- `bool`: True if value is iterable (supports iteration)

**Example:**
```python
result = TypeInference.is_iterable([1, 2, 3])
# Returns: True

result = TypeInference.is_iterable((1, 2, 3))
# Returns: True

result = TypeInference.is_iterable('abc')
# Returns: True

result = TypeInference.is_iterable(123)
# Returns: False
```

#### `TypeInference.is_iterable_not_string(value: Any) -> bool`
Check if value is iterable but not a string.

This is useful for distinguishing between collections (lists, tuples, sets, etc.)
and string values, which are also iterable but often need different handling.

**Parameters:**
- `value` (Any): Value to check

**Returns:**
- `bool`: True if value is iterable and not a string

**Example:**
```python
result = TypeInference.is_iterable_not_string([1, 2, 3])
# Returns: True

result = TypeInference.is_iterable_not_string((1, 2, 3))
# Returns: True

result = TypeInference.is_iterable_not_string({'a': 1})
# Returns: True

result = TypeInference.is_iterable_not_string('abc')
# Returns: False

result = TypeInference.is_iterable_not_string(123)
# Returns: False
```

#### `TypeInference.is_empty(value: Any) -> bool`
Check if value is empty (None, empty string, or empty collection).

This method provides a unified way to check for emptiness across different
types of values, handling None, strings, and collections consistently.

**Parameters:**
- `value` (Any): Value to check for emptiness

**Returns:**
- `bool`: True if value is None, empty string, or empty collection

**Example:**
```python
result = TypeInference.is_empty(None)
# Returns: True

result = TypeInference.is_empty('')
# Returns: True

result = TypeInference.is_empty('   ')
# Returns: True (whitespace-only)

result = TypeInference.is_empty([])
# Returns: True

result = TypeInference.is_empty({})
# Returns: True

result = TypeInference.is_empty(set())
# Returns: True

result = TypeInference.is_empty('abc')
# Returns: False

result = TypeInference.is_empty([1, 2, 3])
# Returns: False
```

## String Class

### Class Description
The `String` class provides low-level string processing utilities with static methods for validation and conversion operations.

### Validation Methods

#### `is_int_like(value: str) -> bool`
Check if a string represents a valid integer.

**Parameters:**
- `value` (str): The string to validate

**Returns:**
- `bool`: True if the string represents a valid integer

**Validation Rules:**
- Optional leading sign (+ or -)
- One or more digits
- No decimal points or other characters

**Example:**
```python
result = String.is_int_like("123")
# Returns: True

result = String.is_int_like("123.45")
# Returns: False
```

#### `is_float_like(value: str) -> bool`
Check if a string represents a valid float.

**Parameters:**
- `value` (str): The string to validate

**Returns:**
- `bool`: True if the string represents a valid float

**Validation Rules:**
- Optional leading sign
- Optional integer part
- Required decimal point with optional fractional part
- Supports scientific notation

**Example:**
```python
result = String.is_float_like("123.45")
# Returns: True

result = String.is_float_like("123")
# Returns: True (integers are valid floats)
```

#### `is_bool_like(value: str) -> bool`
Check if a string represents a valid boolean.

**Parameters:**
- `value` (str): The string to validate

**Returns:**
- `bool`: True if the string represents a valid boolean

**Validation Rules:**
- Case-insensitive: "true", "false", "True", "False", "TRUE", "FALSE"
- Numeric: "1", "0"
- Textual: "yes", "no"

**Example:**
```python
result = String.is_bool_like("true")
# Returns: True

result = String.is_bool_like("True")
# Returns: True

result = String.is_bool_like("1")
# Returns: True
```

#### `is_date_like(value: str) -> bool`
Check if a string represents a valid date.

**Parameters:**
- `value` (str): The string to validate

**Returns:**
- `bool`: True if the string represents a valid date

**Supported Formats:**
- `YYYY-MM-DD` (ISO format)
- `MM/DD/YYYY` (US format)
- `DD/MM/YYYY` (European format)
- `YYYYMMDD` (compact format)
- `YYYY.MM.DD` (dot format)

**Example:**
```python
result = String.is_date_like("2023-01-01")
# Returns: True

result = String.is_date_like("01/01/2023")
# Returns: True
```

#### `is_time_like(value: str) -> bool`
Check if a string represents a valid time.

**Parameters:**
- `value` (str): The string to validate

**Returns:**
- `bool`: True if the string represents a valid time

**Supported Formats:**
- `HH:MM:SS` (24-hour with seconds)
- `HH:MM` (24-hour without seconds)
- `H:MM AM/PM` (12-hour format)
- `HHMMSS` (compact format)

**Example:**
```python
result = String.is_time_like("14:30:00")
# Returns: True

result = String.is_time_like("2:30 PM")
# Returns: True
```

#### `is_datetime_like(value: str) -> bool`
Check if a string represents a valid datetime.

**Parameters:**
- `value` (str): The string to validate

**Returns:**
- `bool`: True if the string represents a valid datetime

**Supported Formats:**
- `YYYY-MM-DDTHH:MM:SS` (ISO format)
- `YYYY-MM-DD HH:MM:SS` (space separated)
- `MM/DD/YYYY HH:MM:SS` (US format)

**Example:**
```python
result = String.is_datetime_like("2023-01-01T12:00:00")
# Returns: True

result = String.is_datetime_like("2023-01-01 12:00:00")
# Returns: True
```

### Conversion Methods

#### `to_int(value: str) -> int | None`
Convert a string to an integer.

**Parameters:**
- `value` (str): The string to convert

**Returns:**
- `int | None`: The integer value, or None if conversion fails

**Example:**
```python
result = String.to_int("123")
# Returns: 123

result = String.to_int("abc")
# Returns: None
```

#### `to_float(value: str) -> float | None`
Convert a string to a float.

**Parameters:**
- `value` (str): The string to convert

**Returns:**
- `float | None`: The float value, or None if conversion fails

**Example:**
```python
result = String.to_float("123.45")
# Returns: 123.45

result = String.to_float("abc")
# Returns: None
```

#### `to_bool(value: str) -> bool | None`
Convert a string to a boolean.

**Parameters:**
- `value` (str): The string to convert

**Returns:**
- `bool | None`: The boolean value, or None if conversion fails

**Conversion Rules:**
- `"true"`, `"True"`, `"TRUE"`, `"1"`, `"yes"`, `"Yes"` → `True`
- `"false"`, `"False"`, `"FALSE"`, `"0"`, `"no"`, `"No"` → `False`

**Example:**
```python
result = String.to_bool("true")
# Returns: True

result = String.to_bool("false")
# Returns: False
```

#### `to_date(value: str) -> date | None`
Convert a string to a date.

**Parameters:**
- `value` (str): The string to convert

**Returns:**
- `date | None`: The date object, or None if conversion fails

**Example:**
```python
result = String.to_date("2023-01-01")
# Returns: datetime.date(2023, 1, 1)

result = String.to_date("invalid")
# Returns: None
```

#### `to_time(value: str) -> time | None`
Convert a string to a time.

**Parameters:**
- `value` (str): The string to convert

**Returns:**
- `time | None`: The time object, or None if conversion fails

**Example:**
```python
result = String.to_time("14:30:00")
# Returns: datetime.time(14, 30, 0)

result = String.to_time("invalid")
# Returns: None
```

#### `to_datetime(value: str) -> datetime | None`
Convert a string to a datetime.

**Parameters:**
- `value` (str): The string to convert

**Returns:**
- `datetime | None`: The datetime object, or None if conversion fails

**Example:**
```python
result = String.to_datetime("2023-01-01T12:00:00")
# Returns: datetime.datetime(2023, 1, 1, 12, 0, 0)

result = String.to_datetime("2023-01-01 12:00:00")
# Returns: datetime.datetime(2023, 1, 1, 12, 0, 0)

result = String.to_datetime("invalid")
# Returns: None
```

### Utility Methods

#### `infer_type(value: str) -> DataType`
Direct type inference for a string value.

**Parameters:**
- `value` (str): The string to analyze

**Returns:**
- `DataType`: The inferred data type

**Example:**
```python
result = String.infer_type("123")
# Returns: DataType.INTEGER

result = String.infer_type("2023-01-01T12:00:00")
# Returns: DataType.DATETIME

result = String.infer_type("2023-01-01 12:00:00")
# Returns: DataType.DATETIME
```

#### `_normalize_input(value: str | bool | None, trim: bool = True) -> str | None`
Normalize input value for type checking operations.

**Parameters:**
- `value` (str | bool | None): The value to normalize
- `trim` (bool): Whether to trim whitespace (default: True)

**Returns:**
- `str | None`: The normalized string value

**Example:**
```python
result = String._normalize_input("  hello  ")
# Returns: "hello"

result = String._normalize_input("  hello  ", trim=False)
# Returns: "  hello  "
```

## DuckTyping Class

### Class Description
The `DuckTyping` class provides comprehensive duck typing utilities for determining object behavior based on available methods rather than inheritance. Duck typing enables more flexible type checking that works with custom objects and third-party classes.

### Features
- List-like behavior detection
- Dictionary-like behavior detection
- Iterability checking
- Collection vs string distinction
- Unified emptiness checking
- Behavioral type analysis

### Static Methods

#### `DuckTyping.is_list_like(value: Any) -> bool`
Check if value behaves like a list (duck typing).

This method performs duck typing to determine if a value has list-like behavior,
checking for the presence of common list methods (append, remove, index).

**Parameters:**
- `value` (Any): Value to check for list-like behavior

**Returns:**
- `bool`: True if value is a list or has list-like behavior (append, remove, index methods)

**Example:**
```python
result = DuckTyping.is_list_like([1, 2, 3])
# Returns: True

result = DuckTyping.is_list_like((1, 2, 3))
# Returns: False

from collections import deque
result = DuckTyping.is_list_like(deque([1, 2, 3]))
# Returns: True
```

#### `DuckTyping.is_dict_like(value: Any) -> bool`
Check if value behaves like a dictionary (duck typing).

This method performs duck typing to determine if a value has dictionary-like behavior,
checking for the presence of common dictionary methods (keys, get, values).

**Parameters:**
- `value` (Any): Value to check for dictionary-like behavior

**Returns:**
- `bool`: True if value is a dict or has dict-like behavior (keys, get, values methods)

**Example:**
```python
result = DuckTyping.is_dict_like({'a': 1})
# Returns: True

result = DuckTyping.is_dict_like([1, 2, 3])
# Returns: False

from collections import OrderedDict
result = DuckTyping.is_dict_like(OrderedDict([('a', 1)]))
# Returns: True
```

#### `DuckTyping.is_iterable(value: Any) -> bool`
Check if value is iterable.

This method determines if a value supports iteration, either through the
Iterable protocol or by having common iteration-related methods.

**Parameters:**
- `value` (Any): Value to check for iterability

**Returns:**
- `bool`: True if value is iterable (supports iteration)

**Example:**
```python
result = DuckTyping.is_iterable([1, 2, 3])
# Returns: True

result = DuckTyping.is_iterable((1, 2, 3))
# Returns: True

result = DuckTyping.is_iterable('abc')
# Returns: True

result = DuckTyping.is_iterable(123)
# Returns: False
```

#### `DuckTyping.is_iterable_not_string(value: Any) -> bool`
Check if value is iterable but not a string.

This is useful for distinguishing between collections (lists, tuples, sets, etc.)
and string values, which are also iterable but often need different handling.

**Parameters:**
- `value` (Any): Value to check

**Returns:**
- `bool`: True if value is iterable and not a string

**Example:**
```python
result = DuckTyping.is_iterable_not_string([1, 2, 3])
# Returns: True

result = DuckTyping.is_iterable_not_string((1, 2, 3))
# Returns: True

result = DuckTyping.is_iterable_not_string({'a': 1})
# Returns: True

result = DuckTyping.is_iterable_not_string('abc')
# Returns: False

result = DuckTyping.is_iterable_not_string(123)
# Returns: False
```

#### `DuckTyping.is_empty(value: Any) -> bool`
Check if value is empty (None, empty string, or empty collection).

This method provides a unified way to check for emptiness across different
types of values, handling None, strings, and collections consistently.

**Parameters:**
- `value` (Any): Value to check for emptiness

**Returns:**
- `bool`: True if value is None, empty string, or empty collection

**Example:**
```python
result = DuckTyping.is_empty(None)
# Returns: True

result = DuckTyping.is_empty('')
# Returns: True

result = DuckTyping.is_empty('   ')
# Returns: True (whitespace-only)

result = DuckTyping.is_empty([])
# Returns: True

result = DuckTyping.is_empty({})
# Returns: True

result = DuckTyping.is_empty(set())
# Returns: True

result = DuckTyping.is_empty('abc')
# Returns: False

result = DuckTyping.is_empty([1, 2, 3])
# Returns: False
```

#### `DuckTyping.get_behavior_type(value: Any) -> str`
Get a string describing the behavioral type of a value.

This method analyzes a value and returns a string describing its
behavioral characteristics based on duck typing.

**Parameters:**
- `value` (Any): Value to analyze

**Returns:**
- `str`: String describing the behavioral type

**Example:**
```python
result = DuckTyping.get_behavior_type([1, 2, 3])
# Returns: 'list-like'

result = DuckTyping.get_behavior_type({'a': 1})
# Returns: 'dict-like'

result = DuckTyping.get_behavior_type('abc')
# Returns: 'string'

result = DuckTyping.get_behavior_type(123)
# Returns: 'scalar'

result = DuckTyping.get_behavior_type(None)
# Returns: 'empty'
```

## DataType Enum

### Enum Description
The `DataType` enum defines all supported data types for type inference and conversion operations.

### Enum Values

| Enum Value | String Value | Description | Python Type |
|------------|--------------|-------------|-------------|
| `DataType.STRING` | `"str"` | Text data | `str` |
| `DataType.INTEGER` | `"int"` | Whole numbers | `int` |
| `DataType.FLOAT` | `"float"` | Decimal numbers | `float` |
| `DataType.BOOLEAN` | `"bool"` | True/false values | `bool` |
| `DataType.DATE` | `"date"` | Calendar dates | `datetime.date` |
| `DataType.TIME` | `"time"` | Time values | `datetime.time` |
| `DataType.DATETIME` | `"datetime"` | Date and time | `datetime.datetime` |
| `DataType.MIXED` | `"mixed"` | Multiple types | N/A |
| `DataType.EMPTY` | `"empty"` | Empty/whitespace strings | `str` |
| `DataType.NONE` | `"none"` | Null values | `None` |

### Enum Methods

#### String Representation
```python
str(DataType.INTEGER)  # "DataType.INTEGER"
```

#### Value Access
```python
DataType.INTEGER.value  # "int"
```

#### Hashable and Comparable
```python
# Can be used as dictionary keys
type_map = {DataType.INTEGER: int, DataType.STRING: str}

# Can be compared
DataType.INTEGER == DataType.INTEGER  # True
DataType.INTEGER != DataType.STRING   # True
```

## Error Handling

### General Error Handling Strategy

The API follows a "graceful degradation" strategy:

1. **No Exceptions**: Public methods never raise exceptions
2. **Fallback Values**: Invalid inputs return safe fallback values
3. **Type Preservation**: Original input types are preserved when conversion fails

### Specific Error Behaviors

#### Type Inference Errors
- Invalid inputs → `DataType.STRING`
- None values → `DataType.STRING`
- Non-string inputs → `DataType.STRING`

#### Type Conversion Errors
- Invalid integers → original string
- Invalid floats → original string
- Invalid booleans → `None`
- Invalid dates → `None`
- Invalid times → `None`
- Invalid datetimes → `None`

#### Collection Analysis Errors
- Empty collections → `DataType.MIXED`
- Collections with invalid items → `DataType.MIXED` (if heterogeneous)

## Performance Characteristics

### Single Value Operations
- **Type Inference**: O(1) - constant time pattern matching
- **Type Conversion**: O(1) - constant time parsing and conversion
- **Memory Usage**: O(1) - minimal additional memory

### Collection Operations
- **Small Collections** (< 10,000 items): O(n) - linear processing
- **Large Collections** (≥ 10,000 items): O(n) with incremental processing
- **Memory Usage**: O(n) - proportional to input size

### Incremental Processing
- **Threshold**: 10,000 items (configurable)
- **Optimization**: Reduces memory usage for large datasets
- **Behavior**: Automatic activation based on input size

## Thread Safety

### Thread Safety Status
- **Instance Methods**: Thread-safe (no shared state)
- **Static Methods**: Thread-safe (pure functions)
- **Class State**: Minimal class-level state, thread-safe access

### Usage in Multi-threaded Environments
```python
import threading
from splurge_typer import TypeInference

def worker_thread(data):
    ti = TypeInference()  # Create instance per thread
    results = [ti.infer_type(item) for item in data]
    return results

# Safe to use across multiple threads
threads = []
for i in range(4):
    thread = threading.Thread(target=worker_thread, args=(data_chunk,))
    threads.append(thread)
    thread.start()
```

## Memory Management

### Memory Usage Patterns
- **Temporary Objects**: Minimal temporary object creation
- **String Operations**: Efficient string handling without unnecessary copying
- **Large Datasets**: Incremental processing to manage memory usage
- **Cleanup**: Automatic cleanup of temporary data structures

### Memory Optimization Tips
```python
# For large datasets, process in chunks
chunk_size = 10000
for i in range(0, len(large_dataset), chunk_size):
    chunk = large_dataset[i:i + chunk_size]
    result = ti.profile_values(chunk)
    # Process result
```

## Version Compatibility

### API Stability
- **Major Version Changes**: Breaking changes to public API
- **Minor Version Changes**: New features, backward compatible
- **Patch Version Changes**: Bug fixes, no API changes

### Backward Compatibility
- Public API maintained across minor versions
- Deprecation warnings for changed functionality
- Migration guides provided for major version changes

## Examples

### Basic Usage
```python
from splurge_typer import TypeInference, DataType

ti = TypeInference()

# Single value inference
print(ti.infer_type("123"))  # DataType.INTEGER
print(ti.convert_value("123"))  # 123

# Collection analysis
data = ["1", "2", "3", "4", "5"]
print(ti.profile_values(data))  # DataType.INTEGER
```

### Advanced Usage
```python
# Multiple data types
mixed_data = ["123", "45.67", "true", "2023-01-01", "hello"]
print(ti.profile_values(mixed_data))  # DataType.MIXED

# Individual processing
for item in mixed_data:
    inferred = ti.infer_type(item)
    converted = ti.convert_value(item)
    print(f"{item} -> {inferred.value}: {converted}")
```

### Static Methods
```python
# Check if value can be inferred
print(TypeInference.can_infer("123"))  # True
print(TypeInference.can_infer("hello"))  # False

# Get processing threshold
threshold = TypeInference.get_incremental_typecheck_threshold()
print(f"Threshold: {threshold}")  # 10000
```

---

*This API specification is comprehensive and covers all public interfaces. For implementation details, see the source code documentation.*
