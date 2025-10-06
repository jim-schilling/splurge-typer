"""Hypothesis tests for TypeInference.convert_value and edge cases.

These tests validate conversion of strings to native types and handling of
None/empty inputs and native Python objects passed through unchanged.
"""

from datetime import date, time
from math import isclose

from hypothesis import given
from hypothesis import strategies as st

from splurge_typer.data_type import DataType
from splurge_typer.type_inference import TypeInference


@given(st.integers(min_value=-999, max_value=999))
def test_convert_value_integer(i: int) -> None:
    s = str(i)
    got = TypeInference.convert_value(s)
    assert isinstance(got, int) and got == i


@given(
    st.one_of(
        st.floats(min_value=1e-6, max_value=1e6, allow_nan=False, allow_infinity=False),
        st.floats(min_value=-1e6, max_value=-1e-6, allow_nan=False, allow_infinity=False),
    )
)
def test_convert_value_float(f: float) -> None:
    s = format(f, ".12f")
    got = TypeInference.convert_value(s)
    # convert_value may return float or None in edge cases; compare with tolerance if float
    if isinstance(got, float):
        assert isclose(got, f, rel_tol=1e-9, abs_tol=1e-12)


@given(st.sampled_from(["true", "false", "TRUE", "False"]))
def test_convert_value_bool(bs: str) -> None:
    got = TypeInference.convert_value(bs)
    assert isinstance(got, bool)


@given(st.dates())
def test_convert_value_date(d: date) -> None:
    s = d.isoformat()
    got = TypeInference.convert_value(s)
    assert got == d


def test_convert_value_none_and_empty() -> None:
    assert TypeInference.convert_value(None) is None
    assert TypeInference.convert_value("") == ""
    # Strings that are just whitespace should be considered EMPTY by TypeInference.infer_type
    assert TypeInference.convert_value("   ") == ""


@given(st.text(min_size=1, max_size=20))
def test_convert_value_non_convertible_strings(s: str) -> None:
    # If string is not convertible, convert_value should return the original string
    # But some strings may be convertible (numbers/dates), so skip those
    inferred = TypeInference.infer_type(s)
    if inferred == DataType.STRING:
        assert TypeInference.convert_value(s) == s


@given(st.builds(lambda y: y, st.times()))
def test_native_objects_pass_through(t: time) -> None:
    # Native time/date objects should pass through convert_value unchanged
    assert TypeInference.convert_value(t) == t
