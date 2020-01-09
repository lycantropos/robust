from typing import Tuple

from hypothesis import given

from robust.hints import Scalar
from robust.utils import two_product
from tests import strategies
from tests.utils import are_non_overlapping_numbers


@given(strategies.scalars_pairs)
def test_basic(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    result = two_product(left, right)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(left)) for element in result)


@given(strategies.scalars_pairs)
def test_properties(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    estimation, tail = two_product(left, right)

    assert estimation + tail == left * right
    assert abs(estimation) >= abs(tail)
    assert are_non_overlapping_numbers(estimation, tail)


@given(strategies.scalars)
def test_left_absorbing_element(scalar: Scalar) -> None:
    assert two_product(0, scalar) == (0, 0)


@given(strategies.scalars)
def test_right_absorbing_element(scalar: Scalar) -> None:
    assert two_product(scalar, 0) == (0, 0)
