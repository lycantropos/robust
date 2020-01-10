from hypothesis import given

from robust.hints import Scalar
from robust.utils import square
from tests import strategies
from tests.utils import are_non_overlapping_numbers


@given(strategies.scalars)
def test_basic(scalar: Scalar) -> None:
    result = square(scalar)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(scalar)) for element in result)


@given(strategies.scalars)
def test_properties(scalar: Scalar) -> None:
    tail, estimation = square(scalar)

    assert estimation + tail == scalar ** 2
    assert abs(estimation) >= abs(tail)
    assert are_non_overlapping_numbers(estimation, tail)
