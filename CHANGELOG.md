# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Calendar Versioning](https://calver.org/) (CalVer).

## [2025.1.0] - 2025-10-05
### Added
- Dev tooling and project configuration
  - Added development dependencies and tool sections to `pyproject.toml` (pytest, pytest-cov, pytest-xdist, hypothesis, mypy, ruff, pre-commit).
  - Added Hypothesis configuration and tuned pytest addopts for parallel test runs.

- Pre-commit and CI
  - Moved pre-commit configuration into a dedicated `.pre-commit-config.yaml` and added local `system` hooks that run `ruff check .`, `mypy splurge_typer`, and `pytest -q -n 4` (with `pass_filenames: false`).

- Domain exceptions
  - Introduced a domain-specific exceptions module `splurge_typer/exceptions.py` with a `SplurgeTyperError` base and specific subclasses (e.g., `SplurgeTyperValueError`, `SplurgeTyperConversionError`, `SplurgeTyperTypeInferenceError`).
  - Exported the new exception types from the package root (`splurge_typer/__init__.py`) for convenient public consumption.

- Property and robust tests
  - Added multiple Hypothesis-based property test modules to exercise parsing and inference logic:
    - `tests/unit/test_string_hypothesis.py`
    - `tests/unit/test_typeinference_hypothesis.py`
    - `tests/unit/test_typeinference_convert_hypothesis.py`
    - `tests/unit/test_typeinference_profile_hypothesis.py`
  - These tests increase randomized coverage for `String` and `TypeInference` helpers and validate incremental behaviour for large datasets.

- Documentation
  - Added a comprehensive API reference at `docs/api/API-REFERENCE.md`.
  - Updated `docs/README-details.md` with a new "Testing strategy" section describing unit/integration/e2e tiers and Hypothesis usage.
  - Linked API docs from the top-level `README.md` and `docs/README-details.md`.

### Changed
- Code quality and docstrings
  - Standardized module, class, and method docstrings across the package to Google-style and improved examples and parameter descriptions.

- Type inference behaviour
  - `TypeInference.profile_values` now raises a domain-specific `SplurgeTyperValueError` when a non-iterable is passed (replaces a generic ValueError at this checkpoint).

- Tests and CI
  - Configured pytest to run tests in parallel (xdist) and added coverage reporting defaults.
  - Integrated ruff auto-fixes and mypy checks into the development workflow.

### Fixed
- Test stability and edge-cases
  - Stabilized Hypothesis strategies to avoid false negatives caused by parser-specific edge cases (e.g., large integers interpreted as times, scientific-notation float formatting) by constraining generated ranges and using fixed-point formatting where appropriate.
  - Addressed intermittent failures by tightening generated inputs and updating unit expectations where the public contract changed (for example, `profile_values` behaviour around mixed date/time formats).

### Testing & Metrics
- Test results (local)
  - Full test suite: 503 passed (local environment during release).
  - Coverage: improved to ~95% overall after adding property tests and focused fixes.


## [2025.0.1] - 2025-09-01

### Documentation
- **Enhanced Docstrings**: Comprehensive review and improvement of all module, class, and method docstrings
  - Updated `type_inference.py` with detailed module overview, performance features, and usage examples
  - Enhanced `TypeInference` class docstring with core capabilities and integration details
  - Improved method docstrings for `convert_value()`, `infer_type()`, `can_infer()`, and `get_incremental_typecheck_threshold()`
  - Verified all other modules (`__init__.py`, `data_type.py`, `duck_typing.py`, `string.py`) have accurate, comprehensive docstrings
- **Documentation Quality**: Ensured all docstrings accurately reflect actual behavior with proper examples and parameter descriptions

---

## [2025.0.0] - 2025-09-01

### Added
- **Initial Release**: Complete type inference and conversion library for Python
- **Data Type Inference**: Automatic detection of data types from string values
  - INTEGER: Whole numbers (`'123'`, `'-456'`, `'00123'`)
  - FLOAT: Decimal numbers (`'1.23'`, `'-4.56'`, `'1.0'`)
  - BOOLEAN: True/false values (`'true'`, `'false'`, `'True'`, `'False'`, `'1'`, `'0'`)
  - DATE: Date values in multiple formats (`'2023-01-01'`, `'01/01/2023'`, `'20230101'`)
  - TIME: Time values (`'14:30:00'`, `'2:30 PM'`, `'143000'`)
  - DATETIME: Combined date and time (`'2023-01-01T12:00:00'`)
  - STRING: Text data that doesn't match other patterns
  - EMPTY: Empty strings or whitespace-only strings
  - NONE: Null values (`'none'`, `'null'`, `None`)
  - MIXED: Collections containing multiple data types

- **Type Conversion**: Convert strings to their inferred Python types
  - Automatic conversion to `int`, `float`, `bool`, `date`, `time`, `datetime`
  - Safe conversion with fallback to original string for invalid inputs

- **Collection Analysis**: Analyze sequences of values to determine dominant types
  - Efficient processing of large datasets (>10,000 items)
  - Incremental processing for optimal performance
  - Mixed type detection for heterogeneous data

- **Comprehensive API**:
  - `TypeInference` class with instance and static methods
  - `String` utility class for low-level string processing
  - `DataType` enum for type classification
  - Full type annotations throughout

- **Robust Parsing**:
  - Support for multiple date/time formats
  - Leading zero handling for numbers
  - Case-insensitive boolean parsing
  - Comprehensive edge case handling

- **Performance Optimized**:
  - Incremental type checking for large datasets
  - Efficient regex patterns for validation
  - Minimal memory footprint

### Features
- **Single Value Inference**: `TypeInference().infer_type('123')` → `DataType.INTEGER`
- **Type Conversion**: `TypeInference().convert_value('123')` → `123`
- **Collection Analysis**: `TypeInference().profile_values(['1', '2', '3'])` → `DataType.INTEGER`
- **Flexible Parsing**: Handles various formats and edge cases
- **Production Ready**: Comprehensive error handling and validation

### Technical Details
- **Python Version**: Compatible with Python 3.10+
- **Dependencies**: No external dependencies (uses only standard library)
- **Architecture**: Clean separation of concerns with dedicated classes
- **Testing**: Comprehensive test suite with 85%+ coverage target
- **Documentation**: Full Google-style docstrings and usage examples

---

## Version History
- **2025.0.1**: Documentation improvements and enhanced docstrings
- **2025.0.0**: Initial release with complete type inference functionality

---

## Contributing
When preparing a new release, update this changelog following the format above.
