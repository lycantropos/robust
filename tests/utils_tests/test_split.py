from hypothesis import given

from robust.hints import Scalar
from robust.utils import split
from tests import strategies
from tests.utils import are_non_overlapping_numbers


@given(strategies.scalars)
def test_basic(scalar: Scalar) -> None:
    result = split(scalar)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(scalar)) for element in result)


@given(strategies.scalars)
def test_properties(scalar: Scalar) -> None:
    low, high = split(scalar)

    assert low + high == scalar
    assert abs(low) <= abs(high)
    assert are_non_overlapping_numbers(low, high)
