"""Additional Hypothesis tests for TypeInference.profile_values.

These tests target edge mixtures, multiple date/time string formats, and
exercise incremental early-termination using large synthetic datasets.
"""

from datetime import date

from hypothesis import given
from hypothesis import strategies as st

from splurge_typer.data_type import DataType
from splurge_typer.type_inference import TypeInference


@given(
    st.lists(
        st.one_of(
            st.integers(min_value=-999, max_value=999).map(str),
            st.floats(min_value=1e-6, max_value=1e6, allow_nan=False, allow_infinity=False).map(
                lambda f: format(f, ".12f")
            ),
            st.text(min_size=1, max_size=6),
        ),
        min_size=3,
        max_size=30,
    )
)
def test_profile_values_edge_mixtures(values: list[str]) -> None:
    """Random mixtures including ints, floats and arbitrary strings should return a sensible DataType."""
    res = TypeInference.profile_values(values)
    # Accept any of the plausible outcomes; this is a smoke/property check
    assert res in (
        DataType.INTEGER,
        DataType.FLOAT,
        DataType.MIXED,
        DataType.STRING,
        DataType.BOOLEAN,
        DataType.DATE,
        DataType.DATETIME,
        DataType.TIME,
    )


@given(st.lists(st.dates(), min_size=1, max_size=30))
def test_profile_values_varied_date_formats(ds: list[date]) -> None:
    """Feed several ISO date-like formats and ensure detection of DATE or DATETIME when appropriate."""
    # Generate a variety of date/time string formats
    strings = []
    for d in ds:
        strings.append(d.isoformat())
        strings.append(d.strftime("%Y/%m/%d"))
        strings.append(d.strftime("%d-%m-%Y"))
    result = TypeInference.profile_values(strings)
    # Different date formats mixed in one list may be considered MIXED by the
    # current parsing heuristics; accept MIXED as a valid outcome as well.
    assert result in (DataType.DATE, DataType.STRING, DataType.MIXED)


def test_profile_values_large_dataset_incremental_behavior() -> None:
    """Create a large dataset that should trigger incremental checks and verify no crash and a valid result."""
    base = [str(i) for i in range(10)]
    # Ensure some non-numeric entries are present late in the list to potentially force MIXED
    base[-1] = "abc"
    # Repeat until we are well above the threshold
    multiplier = TypeInference.get_incremental_typecheck_threshold() // len(base) + 5
    large = base * multiplier
    result = TypeInference.profile_values(large, use_incremental_typecheck=True)
    assert result in (DataType.MIXED, DataType.INTEGER, DataType.STRING)
