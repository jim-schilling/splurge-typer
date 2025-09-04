# splurge-typer

**Type Inference and Conversion Library for Python**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

splurge-typer is a comprehensive Python library for inferring data types from string values and converting between different data representations. It can analyze individual string values or entire collections to determine the most appropriate Python data type.

## Features

- **Single Value Inference**: Automatically detect the data type of individual string values
- **Collection Analysis**: Analyze sequences of values to determine dominant types
- **Type Conversion**: Convert strings to their inferred Python types
- **Comprehensive Type Support**: Handles integers, floats, booleans, dates, times, datetimes, and more
- **Performance Optimized**: Includes incremental processing for large datasets
- **Flexible Parsing**: Supports multiple date/time formats and handles edge cases

## Installation

```bash
# Clone the repository
git clone https://github.com/jim-schilling/splurge-typer.git
cd splurge-typer

# Install in development mode
pip install -e .
```

## Quick Start

### Basic Usage

```python
from splurge_typer import TypeInference, DataType

# Create a type inference instance
ti = TypeInference()

# Single value inference
print(ti.infer_type('123'))        # DataType.INTEGER
print(ti.infer_type('1.23'))       # DataType.FLOAT
print(ti.infer_type('true'))       # DataType.BOOLEAN
print(ti.infer_type('2023-01-01')) # DataType.DATE

# Type conversion
print(ti.convert_value('123'))        # 123 (int)
print(ti.convert_value('1.23'))       # 1.23 (float)
print(ti.convert_value('true'))       # True (bool)
```

### Collection Analysis

```python
# Analyze collections of values
values1 = ['1', '2', '3']
print(ti.profile_values(values1))  # DataType.INTEGER

values2 = ['1.1', '2.2', '3.3']
print(ti.profile_values(values2))  # DataType.FLOAT

values3 = ['1', '2.2', 'hello']
print(ti.profile_values(values3))  # DataType.MIXED
```

## Supported Data Types

The library can infer the following data types:

- `INTEGER`: Whole numbers (`'123'`, `'-456'`, `'00123'`)
- `FLOAT`: Decimal numbers (`'1.23'`, `'-4.56'`, `'1.0'`)
- `BOOLEAN`: True/false values (`'true'`, `'false'`, `'True'`, `'False'`)
- `DATE`: Date values in various formats (`'2023-01-01'`, `'01/01/2023'`, `'20230101'`)
- `TIME`: Time values (`'14:30:00'`, `'2:30 PM'`, `'143000'`)
- `DATETIME`: Combined date and time (`'2023-01-01T12:00:00'`, `'2023-01-01 12:00:00'`)
- `STRING`: Text data that doesn't match other patterns
- `EMPTY`: Empty strings or whitespace-only strings
- `NONE`: Null values (`'none'`, `'null'`, `None`)
- `MIXED`: Collections containing multiple data types

## Advanced Usage

### Handling Edge Cases

```python
# Leading zeros are handled correctly
print(ti.infer_type('00123'))  # DataType.INTEGER

# Invalid dates fall back to string
print(ti.infer_type('2023-13-01'))  # May be interpreted as date in some formats

# Mixed collections
mixed_values = ['123', 'abc', '2023-01-01']
print(ti.profile_values(mixed_values))  # DataType.MIXED
```

### Performance Considerations

For large datasets (>10,000 items), the library automatically enables incremental type checking for better performance:

```python
large_dataset = [str(i) for i in range(50000)]
result = ti.profile_values(large_dataset)  # Uses optimized incremental processing
```

## API Reference

### TypeInference Class

#### Methods

- `infer_type(value: str) -> DataType`: Infer type of a single value
- `convert_value(value: Any) -> Any`: Convert value to its inferred type
- `profile_values(values: Iterable[Any]) -> DataType`: Analyze a collection of values

### String Class

Low-level string processing utilities:

- `is_int_like()`, `is_float_like()`, `is_bool_like()`, etc.
- `to_int()`, `to_float()`, `to_bool()`, etc.
- `infer_type()` - direct type inference

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Jim Schilling (c) 2025
