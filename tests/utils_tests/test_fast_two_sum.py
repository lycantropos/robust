from typing import Tuple

from hypothesis import given

from robust.hints import Scalar
from robust.utils import fast_two_sum
from tests import strategies
from tests.utils import are_non_overlapping_numbers


@given(strategies.scalars_pairs)
def test_basic(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    result = fast_two_sum(left, right)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(left)) for element in result)


@given(strategies.reverse_sorted_by_modulus_scalars_pairs)
def test_properties(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    tail, estimation = fast_two_sum(left, right)

    assert estimation + tail == left + right
    assert abs(estimation) >= abs(tail)
    assert are_non_overlapping_numbers(estimation, tail)


@given(strategies.scalars)
def test_left_neutral_element(scalar: Scalar) -> None:
    assert fast_two_sum(0, scalar) == (0, scalar)


@given(strategies.scalars)
def test_right_neutral_element(scalar: Scalar) -> None:
    assert fast_two_sum(scalar, 0) == (0, scalar)
