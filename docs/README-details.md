# splurge-typer - Detailed Project Documentation

## Project Overview

**splurge-typer** is a comprehensive Python library for automatic type inference and conversion from string values. It provides robust utilities for analyzing individual string values or entire collections to determine the most appropriate Python data type, with efficient conversion capabilities.

## Core Features

### 🔍 **Type Inference Engine**
- **Automatic Detection**: Intelligently identifies data types from string representations
- **Multiple Format Support**: Handles various date/time formats, number representations, and boolean values
- **Edge Case Handling**: Robust processing of malformed or ambiguous data
- **Performance Optimized**: Efficient algorithms for large-scale data processing

### 🔄 **Type Conversion System**
- **Safe Conversion**: Converts strings to their inferred Python types with error handling
- **Fallback Mechanism**: Gracefully handles invalid inputs by returning original strings
- **Type Preservation**: Maintains data integrity during conversion process

### 📊 **Collection Analysis**
- **Bulk Processing**: Analyzes entire datasets to determine dominant types
- **Incremental Processing**: Optimized for large datasets (>10,000 items)
- **Mixed Type Detection**: Identifies heterogeneous data collections

## Supported Data Types

| Data Type | Examples | Python Type | Notes |
|-----------|----------|-------------|--------|
| **INTEGER** | `'123'`, `'-456'`, `'00123'` | `int` | Handles leading zeros |
| **FLOAT** | `'1.23'`, `'-4.56'`, `'1.0'` | `float` | Supports scientific notation |
| **BOOLEAN** | `'true'`, `'false'`, `'yes'`, `'no'` | `bool` | Case-insensitive, multiple formats |
| **DATE** | `'2023-01-01'`, `'01/01/2023'` | `date` | Multiple format support |
| **TIME** | `'14:30:00'`, `'2:30 PM'` | `time` | 12/24 hour formats |
| **DATETIME** | `'2023-01-01T12:00:00'`, `'2023-01-01 12:00:00'` | `datetime` | Combined date/time |
| **STRING** | `'hello'`, `'any text'` | `str` | Default for unmatched patterns |
| **EMPTY** | `''`, `'   '` | `str` | Empty/whitespace strings |
| **NONE** | `'none'`, `'null'` | `None` | Null value representations |
| **MIXED** | `['1', 'hello', 'true']` | N/A | Heterogeneous collections |

## API Reference

### TypeInference Class

The main interface for type inference and conversion operations.

#### Constructor
```python
ti = TypeInference()
```

#### Methods

##### `infer_type(value: str) -> DataType`
Infer the data type of a single string value.

**Parameters:**
- `value` (str): The string value to analyze

**Returns:**
- `DataType`: The inferred data type

**Example:**
```python
ti.infer_type('123')  # DataType.INTEGER
ti.infer_type('2023-01-01')  # DataType.DATE
```

##### `convert_value(value: Any) -> Any`
Convert a value to its inferred Python type.

**Parameters:**
- `value` (Any): The value to convert

**Returns:**
- `Any`: The converted value in its appropriate Python type

**Example:**
```python
ti.convert_value('123')  # 123 (int)
ti.convert_value('true')  # True (bool)
ti.convert_value('2023-01-01')  # date(2023, 1, 1)
```

##### `profile_values(values: Iterable[Any]) -> DataType`
Analyze a collection of values to determine the dominant type.

**Parameters:**
- `values` (Iterable[Any]): Collection of values to analyze

**Returns:**
- `DataType`: The dominant data type in the collection

**Example:**
```python
ti.profile_values(['1', '2', '3'])  # DataType.INTEGER
ti.profile_values(['1', 'hello'])  # DataType.MIXED
```

#### Static Methods

##### `TypeInference.can_infer(value: Any) -> bool`
Check if a value can be inferred as a specific type.

##### `TypeInference.get_incremental_typecheck_threshold() -> int`
Get the threshold for incremental type checking (default: 10,000).

### String Class

Low-level string processing utilities.

#### Validation Methods
- `is_int_like(value: str) -> bool`: Check if string represents an integer
- `is_float_like(value: str) -> bool`: Check if string represents a float
- `is_bool_like(value: str) -> bool`: Check if string represents a boolean
- `is_date_like(value: str) -> bool`: Check if string represents a date
- `is_time_like(value: str) -> bool`: Check if string represents a time
- `is_datetime_like(value: str) -> bool`: Check if string represents a datetime

#### Conversion Methods
- `to_int(value: str) -> int | None`: Convert to integer
- `to_float(value: str) -> float | None`: Convert to float
- `to_bool(value: str) -> bool | None`: Convert to boolean
- `to_date(value: str) -> date | None`: Convert to date
- `to_time(value: str) -> time | None`: Convert to time
- `to_datetime(value: str) -> datetime | None`: Convert to datetime

#### Utility Methods
- `infer_type(value: str) -> DataType`: Direct type inference
- `_normalize_input(value: str | bool | None, trim: bool = True) -> str | None`: Input normalization

### DataType Enum

Enumeration of supported data types.

```python
class DataType(Enum):
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
```

## Usage Examples

### Basic Usage

```python
from splurge_typer import TypeInference, DataType

# Create instance
ti = TypeInference()

# Single value inference
print(ti.infer_type('123'))        # DataType.INTEGER
print(ti.infer_type('1.23'))       # DataType.FLOAT
print(ti.infer_type('true'))       # DataType.BOOLEAN
print(ti.infer_type('2023-01-01')) # DataType.DATE

# Type conversion
print(ti.convert_value('123'))        # 123
print(ti.convert_value('1.23'))       # 1.23
print(ti.convert_value('true'))       # True
print(ti.convert_value('2023-01-01')) # datetime.date(2023, 1, 1)
```

### Collection Analysis

```python
# Analyze collections
values1 = ['1', '2', '3']
print(ti.profile_values(values1))  # DataType.INTEGER

values2 = ['1.1', '2.2', '3.3']
print(ti.profile_values(values2))  # DataType.FLOAT

values3 = ['1', '2.2', 'hello']
print(ti.profile_values(values3))  # DataType.MIXED
```

### Advanced Usage

```python
# Handle edge cases
print(ti.infer_type('00123'))      # DataType.INTEGER (leading zeros)
print(ti.infer_type('   '))        # DataType.EMPTY (whitespace)
print(ti.infer_type('none'))       # DataType.NONE (null values)

# Boolean variations
print(ti.convert_value('TRUE'))    # True
print(ti.convert_value('False'))   # False
print(ti.convert_value('1'))       # True
print(ti.convert_value('0'))       # False

# Multiple date formats
print(ti.convert_value('2023-01-01'))    # date(2023, 1, 1)
print(ti.convert_value('01/01/2023'))    # date(2023, 1, 1)
print(ti.convert_value('20230101'))      # date(2023, 1, 1)
```

### Performance Considerations

```python
# Large datasets automatically use optimized processing
large_dataset = [str(i) for i in range(50000)]
result = ti.profile_values(large_dataset)  # Uses incremental processing
print(result)  # DataType.INTEGER

# Threshold can be checked
threshold = TypeInference.get_incremental_typecheck_threshold()
print(f"Threshold: {threshold}")  # 10000
```

## Technical Specifications

### Performance Characteristics
- **Time Complexity**: O(n) for collection analysis, O(1) for single value inference
- **Space Complexity**: O(1) additional space for single values, O(n) for collections
- **Incremental Threshold**: 10,000 items (configurable)

### Error Handling
- **Invalid Inputs**: Gracefully handles None, non-string inputs
- **Malformed Data**: Returns STRING type for unrecognized patterns
- **Type Conversion**: Safe conversion with None return for invalid operations

### Format Support
- **Date Formats**: YYYY-MM-DD, MM/DD/YYYY, DD/MM/YYYY, YYYYMMDD, etc.
- **Time Formats**: HH:MM:SS, H:MM AM/PM, HHMMSS (compact)
- **Boolean Formats**: true/false, True/False, 1/0, yes/no (case-insensitive)

### Dependencies
- **Python**: 3.10+
- **Standard Library**: datetime, re, typing, collections.abc
- **External**: None (pure Python implementation)

## Testing and Quality Assurance

### Test Coverage
- **Unit Tests**: Individual component testing
- **Integration Tests**: Component interaction testing
- **End-to-End Tests**: Real-world scenario testing
- **Coverage Target**: 85% minimum

### Test Categories
- **Data Type Validation**: Comprehensive type detection testing
- **Conversion Accuracy**: Verify correct type conversion
- **Edge Cases**: Boundary condition and error handling
- **Performance**: Large dataset processing verification
- **Integration**: Full workflow testing

## Architecture and Design

### Design Principles
- **SOLID**: Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion
- **DRY**: Don't repeat yourself - shared utilities and patterns
- **KISS**: Keep it simple and straightforward
- **Fail Fast**: Early validation and error detection

### Code Structure
```
splurge_typer/
├── __init__.py          # Package initialization and exports
├── data_type.py         # DataType enum definition
├── string.py            # String processing utilities
└── type_inference.py    # Main TypeInference class
```

### Class Responsibilities
- **DataType**: Type enumeration and classification
- **String**: Low-level string validation and conversion
- **TypeInference**: High-level interface and orchestration

## Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/jim-schilling/splurge-typer.git
cd splurge-typer

# Install in development mode
pip install -e .

# Run tests
pytest

# Run with coverage
pytest --cov=splurge_typer --cov-report=html
```

### Code Standards
- **PEP 8**: Python style guide compliance
- **Type Hints**: Full type annotation coverage
- **Docstrings**: Google-style documentation
- **Testing**: pytest with comprehensive coverage

## License and Attribution

**License**: MIT License
**Author**: Jim Schilling
**Copyright**: © 2025 Jim Schilling

This project is licensed under the MIT License - see the LICENSE file for details.

---

*For API documentation and additional examples, see the main README.md file.*
