from typing import Tuple

from hypothesis import given

from robust.hints import Scalar
from robust.utils import fast_two_sum
from tests import strategies


@given(strategies.scalars_pairs)
def test_basic(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    result = fast_two_sum(left, right)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(left)) for element in result)


@given(strategies.scalars)
def test_left_neutral_element(scalar: Scalar) -> None:
    assert fast_two_sum(0, scalar) == (scalar, 0)


@given(strategies.scalars)
def test_right_neutral_element(scalar: Scalar) -> None:
    assert fast_two_sum(scalar, 0) == (scalar, 0)
