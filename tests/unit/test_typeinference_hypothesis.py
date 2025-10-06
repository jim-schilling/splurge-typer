"""Hypothesis-based tests for TypeInference.profile_values.

These property tests exercise collection profiling logic including
incremental early-termination behavior and special-case all-digit handling.
"""

from datetime import date

from hypothesis import given
from hypothesis import strategies as st

from splurge_typer.data_type import DataType
from splurge_typer.type_inference import TypeInference


@given(st.lists(st.integers(min_value=-999, max_value=999), min_size=1, max_size=50))
def test_profile_values_all_integers(xs: list[int]) -> None:
    """A list of integer-like values should profile as INTEGER."""
    strs = [str(x) for x in xs]
    assert TypeInference.profile_values(strs) == DataType.INTEGER


@given(
    st.lists(
        st.one_of(
            st.floats(min_value=1e-6, max_value=1e6, allow_nan=False, allow_infinity=False),
            st.floats(min_value=-1e6, max_value=-1e-6, allow_nan=False, allow_infinity=False),
        ),
        min_size=1,
        max_size=50,
    )
)
def test_profile_values_all_floats(xs: list[float]) -> None:
    """A list of float-like values should profile as FLOAT (or MIXED if ints present)."""
    strs = [format(x, ".12f") for x in xs]
    result = TypeInference.profile_values(strs)
    assert result in (DataType.FLOAT, DataType.MIXED)


@given(st.lists(st.text(min_size=1, max_size=10), min_size=2, max_size=50))
def test_profile_values_mixed_string_and_numbers(values: list[str]) -> None:
    """If a list contains strings and numeric-like strings, result may be MIXED."""
    # Inject some numeric strings into the sampled list to create mixed datasets
    # Guarantee two injected numeric-like strings so the list becomes mixed
    values[0] = "123"
    values[1] = "4.56"

    result = TypeInference.profile_values(values)
    assert result in (DataType.MIXED, DataType.STRING, DataType.FLOAT, DataType.INTEGER)


@given(st.lists(st.sampled_from(["true", "false", "TRUE", "False"]), min_size=1, max_size=50))
def test_profile_values_booleans(bs: list[str]) -> None:
    """Lists of boolean-like strings should profile as BOOLEAN."""
    assert TypeInference.profile_values(bs) == DataType.BOOLEAN


@given(st.lists(st.dates(), min_size=1, max_size=50))
def test_profile_values_dates(ds: list[date]) -> None:
    """Date objects and their isoformat strings should be handled as DATE."""
    strs = [d.isoformat() for d in ds]
    assert TypeInference.profile_values(strs) == DataType.DATE


def test_profile_values_incremental_mixed_detection() -> None:
    """Construct a dataset where early incremental detection should return MIXED."""
    # Start with numeric-like values then add a string to force MIXED early
    nums = [str(i) for i in range(10)]
    # Insert a clearly-string value before the first checkpoint (25%)
    mixed = nums.copy()
    mixed.insert(1, "not-a-number")
    # Enable incremental checks by passing a list longer than threshold artificially
    # Use the real threshold to avoid magic numbers
    large = mixed * (TypeInference.get_incremental_typecheck_threshold() // len(mixed) + 1)
    got = TypeInference.profile_values(large, use_incremental_typecheck=True)
    assert got == DataType.MIXED
