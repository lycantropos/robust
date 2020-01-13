from typing import Tuple

from hypothesis import given

from robust.hints import Scalar
from robust.utils import (fast_two_sum,
                          two_sum)
from tests import strategies
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)


@given(strategies.scalars_pairs)
def test_basic(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    result = two_sum(left, right)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(left)) for element in result)


@given(strategies.scalars_pairs)
def test_properties(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    result = two_sum(left, right)

    assert sum(result) == left + right
    assert is_sorted_by_magnitude_expansion(result)
    assert is_non_overlapping_expansion(result)


@given(strategies.reverse_sorted_by_modulus_scalars_pairs)
def test_connection_with_fast_two_sum(scalars_pair: Tuple[Scalar, Scalar]
                                      ) -> None:
    left, right = scalars_pair

    assert two_sum(left, right) == fast_two_sum(left, right)
