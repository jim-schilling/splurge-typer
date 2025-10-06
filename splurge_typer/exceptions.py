"""Custom exception classes for splurge-typer package.

This module defines a hierarchy of custom exceptions for proper error handling
and user-friendly error messages throughout the package.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations


class SplurgeTyperError(Exception):
    """
    Base exception class for all splurge-typer errors.

    This is the root exception that all other splurge exceptions inherit from,
    allowing users to catch all splurge-related errors with a single except clause.
    """

    def __init__(self, message: str, details: str | None = None) -> None:
        """
        Initialize SplurgeTyperError.

        Args:
            message: Human-readable error message
            details: Additional technical details for debugging
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message


class SplurgeTyperFileNotFoundError(SplurgeTyperError):
    """Raised when an expected file cannot be found.

    Example:
        raise SplurgeTyperFileNotFoundError("Config file not found", details=path)
    """


class SplurgeTyperTypeInferenceError(SplurgeTyperError):
    """Raised when type inference fails unexpectedly for a value."""


class SplurgeTyperConversionError(SplurgeTyperError):
    """Raised when a conversion from string to a native type fails."""


class SplurgeTyperValueError(SplurgeTyperError):
    """Raised when input value is invalid for the requested operation."""


class SplurgeTyperConfigurationError(SplurgeTyperError):
    """Raised for invalid or missing configuration/state."""


class SplurgeTyperUnsupportedTypeError(SplurgeTyperError):
    """Raised when an operation is requested for a type that is unsupported."""


class SplurgeTyperDataValidationError(SplurgeTyperError):
    """Raised when data fails validation checks (schema/constraints)."""
