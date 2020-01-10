from hypothesis import given

from robust.hints import Scalar
from robust.utils import square
from tests import strategies
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)


@given(strategies.scalars)
def test_basic(scalar: Scalar) -> None:
    result = square(scalar)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(scalar)) for element in result)


@given(strategies.scalars)
def test_properties(scalar: Scalar) -> None:
    result = square(scalar)

    assert sum(result) == scalar * scalar
    assert is_sorted_by_magnitude_expansion(result)
    assert is_non_overlapping_expansion(result)
