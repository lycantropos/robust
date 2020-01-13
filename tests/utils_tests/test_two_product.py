from typing import Tuple

from hypothesis import given

from robust.hints import Scalar
from robust.utils import two_product
from tests import strategies
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)


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

    result = two_product(left, right)

    assert sum(result) == left * right
    assert is_sorted_by_magnitude_expansion(result)
    assert is_non_overlapping_expansion(result)
