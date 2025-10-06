# splurge-typer API Reference

This document describes the public API of the `splurge_typer` package: modules, classes, enums, and functions you should use as a consumer. It includes examples, typical errors, and guidance for common tasks.

## Table of Contents

- Overview
- Installation
- Quick Start
- Modules
  - splurge_typer.DataType
  - splurge_typer.String
  - splurge_typer.DuckTyping
  - splurge_typer.TypeInference
- Examples
  - Single value inference and conversion
  - Collection profiling
- Error handling and edge cases
- Contributing and style

---

## Overview

`splurge_typer` is a small, focused library for inferring data types from values (primarily strings) and converting values to their most appropriate native Python types. It supports booleans, integers, floats, dates, times, datetimes, and handles empty and None values gracefully.

The library is intentionally light-weight and designed for easy integration into data pipelines and ETL workflows.

## Installation

Install from source (recommended in a virtual environment):

```bash
python -m pip install -e .[dev]
```

This also installs the recommended dev dependencies (pytest, mypy, ruff, hypothesis, pre-commit, and others).

## Quick Start

```python
from splurge_typer import TypeInference, String, DataType

# Single value
print(TypeInference.infer_type('123'))        # DataType.INTEGER
print(TypeInference.convert_value('123'))     # 123

# Use low-level helpers
print(String.is_date_like('2023-01-01'))      # True
print(String.to_date('2023-01-01'))           # datetime.date(2023, 1, 1)
```

## Modules

### splurge_typer.DataType

Enum: DataType

Description: Enumeration of supported data types used for inference and conversion.

Members:
- STRING: Text data
- INTEGER: Whole numbers
- FLOAT: Decimal numbers
- BOOLEAN: True/False values
- DATE: Calendar dates
- TIME: Time values
- DATETIME: Combined date and time
- MIXED: Multiple types in a collection
- EMPTY: Empty values
- NONE: Null/None values

Usage:

```python
from splurge_typer import DataType

if some_type == DataType.INTEGER:
    # handle integer
    pass
```

### splurge_typer.String

Class: String

Description: Helper class with classmethods for detecting and converting string values.

Common methods:

- is_bool_like(value, *, trim=True) -> bool
- is_none_like(value, *, trim=True) -> bool
- is_empty_like(value, *, trim=True) -> bool
- is_float_like(value, *, trim=True) -> bool
- is_int_like(value, *, trim=True) -> bool
- is_numeric_like(value, *, trim=True) -> bool
- is_date_like(value, *, trim=True) -> bool
- is_time_like(value, *, trim=True) -> bool
- is_datetime_like(value, *, trim=True) -> bool
- to_bool(value, *, default=None, trim=True) -> bool|None
- to_float(value, *, default=None, trim=True) -> float|None
- to_int(value, *, default=None, trim=True) -> int|None
- to_date(value, *, default=None, trim=True) -> date|None
- to_datetime(value, *, default=None, trim=True) -> datetime|None
- to_time(value, *, default=None, trim=True) -> time|None
- infer_type(value, *, trim=True) -> DataType
- infer_type_name(value, *, trim=True) -> str

Notes:
- `infer_type` returns a `DataType` representing the most likely type for the value.
- Conversion helpers return `default` when conversion fails (default is None).

Examples:

```python
from splurge_typer import String

String.is_int_like('123')       # True
String.to_int('123')            # 123
String.is_date_like('2023-01-01')
String.to_date('2023-01-01')
```

Errors:
- Conversion methods return the `default` value on failure rather than raising.

### splurge_typer.DuckTyping

Class: DuckTyping

Description: Static helpers for duck-typing checks (list-like, dict-like, iterable, empty).

Common methods:
- is_list_like(value) -> bool
- is_dict_like(value) -> bool
- is_iterable(value) -> bool
- is_iterable_not_string(value) -> bool
- is_empty(value) -> bool
- get_behavior_type(value) -> str

Examples:

```python
from splurge_typer import DuckTyping

DuckTyping.is_list_like([1,2,3])        # True
DuckTyping.is_dict_like({'a': 1})       # True
DuckTyping.is_empty('')                 # True
```

### splurge_typer.TypeInference

Class: TypeInference

Description: High-level API for inferring types for single values and collections, and converting values to native types.

Key methods:

- get_incremental_typecheck_threshold() -> int
  - Returns the threshold used for incremental checks when profiling large datasets.

- can_infer(value) -> bool
  - Returns True if a string value can be inferred to a specific non-string type.

- infer_type(value) -> DataType
  - Infer the type for a single value.

- convert_value(value) -> Any
  - Convert a value to its inferred native type.

- profile_values(values, *, trim=True, use_incremental_typecheck=True) -> DataType
  - Infer the dominant type for a collection of values.

- Several convenience static wrappers that delegate to DuckTyping for behavior checks.

Examples:

```python
from splurge_typer import TypeInference

# Single value
TypeInference.infer_type('123')       # DataType.INTEGER
TypeInference.convert_value('123')    # 123

# Collection profiling
TypeInference.profile_values(['1','2','3'])  # DataType.INTEGER
```

Errors and edge cases

- Most conversion helpers return a default value (None by default) instead of raising.
- `profile_values` raises ValueError if the provided `values` is not iterable.
- `infer_type` and `String` helpers return `DataType.STRING` for unknown patterns.

Contributing

The project uses ruff, mypy, pytest, pre-commit, and hypothesis for development. See `pyproject.toml` for tool configuration.

If you make changes to public APIs, update this reference and add examples in `docs/api/`.
