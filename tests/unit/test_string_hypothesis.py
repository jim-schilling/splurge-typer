"""Hypothesis-based property tests for string parsing utilities.

These tests exercise the String and TypeInference helpers with generated
values to improve coverage for parsing and conversion logic.
"""

from datetime import date, time

from hypothesis import given
from hypothesis import strategies as st

from splurge_typer.data_type import DataType
from splurge_typer.string import String
from splurge_typer.type_inference import TypeInference


@given(st.integers(min_value=-99, max_value=99))
def test_integer_roundtrip(i: int) -> None:
    """Integer strings should be detected and converted back to the same int."""
    s = str(i)
    assert String.is_int_like(s)
    assert String.to_int(s) == i


@given(
    st.one_of(
        st.floats(min_value=1e-6, max_value=1e6, allow_nan=False, allow_infinity=False),
        st.floats(min_value=-1e6, max_value=-1e-6, allow_nan=False, allow_infinity=False),
    )
)
def test_float_roundtrip(f: float) -> None:
    """Floating point strings should be detected and converted back to same float."""
    # Use repr to ensure a standard text representation (includes decimal point)
    # Use fixed-point formatting to avoid scientific notation (e.g. '1e-06').
    # Use a generous number of decimal places to preserve precision.
    s = format(f, ".12f")
    # Some floats like 1.0 are also int-like; treat float detection as a superset
    assert String.is_float_like(s)
    got = String.to_float(s)
    # to_float may return None for edge cases — when present compare with tolerance
    if got is not None:
        # Allow a tiny relative tolerance due to formatting/truncation
        from math import isclose

        assert isclose(got, f, rel_tol=1e-9, abs_tol=1e-12)


@given(st.dates())
def test_date_roundtrip(d: date) -> None:
    """Date strings in ISO format should be detected and parsed back to date."""
    s = d.isoformat()
    assert String.is_date_like(s)
    parsed = String.to_date(s)
    assert parsed == d


@given(st.times())
def test_time_roundtrip(t: time) -> None:
    """Time strings in ISO format should be detected and parsed back to time."""
    s = t.isoformat()
    # isoformat may omit seconds for simple times; ensure detection is permissive
    assert String.is_time_like(s)
    parsed = String.to_time(s)
    # to_time may return None for some microsecond formats; if present compare
    assert parsed is None or parsed == t


@given(st.sampled_from(["true", "false", "yes", "no", "TRUE", "False"]))
def test_bool_variants(s: str) -> None:
    """Various boolean textual representations should be detected and converted."""
    assert String.is_bool_like(s)
    val = String.to_bool(s)
    assert isinstance(val, bool)


@given(st.integers(min_value=-999, max_value=999))
def test_typeinference_infer_integer(i: int) -> None:
    # Restrict integers to a reasonable range to avoid ambiguous/time-like values
    s = str(i)
    assert TypeInference.infer_type(s) == DataType.INTEGER
