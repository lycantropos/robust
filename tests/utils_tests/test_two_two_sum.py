from numbers import Real
from typing import Tuple

from hypothesis import given

from robust.utils import two_two_sum
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)
from . import strategies


@given(strategies.non_overlapping_real_numbers_pairs_pairs)
def test_basic(numbers_pairs_pair: Tuple[Tuple[Real, Real],
                                         Tuple[Real, Real]]) -> None:
    (left_tail, left), (right_tail, right) = numbers_pairs_pair

    result = two_two_sum(left_tail, left, right_tail, right)

    assert isinstance(result, tuple)
    assert len(result) == 4
    assert all(isinstance(element, type(left)) for element in result)


@given(strategies.non_overlapping_real_numbers_pairs_pairs)
def test_properties(numbers_pairs_pair: Tuple[Tuple[Real, Real],
                                              Tuple[Real, Real]]) -> None:
    (left_tail, left), (right_tail, right) = numbers_pairs_pair

    result = two_two_sum(left_tail, left, right_tail, right)

    assert is_sorted_by_magnitude_expansion(result)
    assert is_non_overlapping_expansion(result)
