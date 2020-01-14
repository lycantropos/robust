from numbers import Real
from typing import Tuple

from hypothesis import given

from robust.utils import two_sum
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)
from . import strategies


@given(strategies.numbers_pairs)
def test_basic(numbers_pair: Tuple[Real, Real]) -> None:
    left, right = numbers_pair

    result = two_sum(left, right)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(left)) for element in result)


@given(strategies.numbers_pairs)
def test_properties(numbers_pair: Tuple[Real, Real]) -> None:
    left, right = numbers_pair

    result = two_sum(left, right)

    assert sum(result) == left + right
    assert is_sorted_by_magnitude_expansion(result)
    assert is_non_overlapping_expansion(result)
