from numbers import Real

from hypothesis import given

from robust.utils import split
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)
from . import strategies


@given(strategies.numbers)
def test_basic(number: Real) -> None:
    result = split(number)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(number)) for element in result)


@given(strategies.numbers)
def test_properties(number: Real) -> None:
    result = split(number)

    assert sum(result) == number
    assert is_sorted_by_magnitude_expansion(result)
    assert is_non_overlapping_expansion(result)
