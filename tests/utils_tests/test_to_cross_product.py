from numbers import Real
from typing import Tuple

from hypothesis import given

from robust.utils import to_cross_product
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)
from . import strategies


@given(strategies.numbers_quadruples)
def test_basic(numbers_quadruple: Tuple[Real, Real, Real, Real]
               ) -> None:
    (minuend_multiplier_x, minuend_multiplier_y,
     subtrahend_multiplier_x, subtrahend_multiplier_y) = numbers_quadruple

    result = to_cross_product(minuend_multiplier_x, minuend_multiplier_y,
                              subtrahend_multiplier_x, subtrahend_multiplier_y)

    assert isinstance(result, tuple)
    assert len(result) == 4
    assert all(isinstance(element, type(minuend_multiplier_x))
               for element in result)


@given(strategies.numbers_quadruples)
def test_properties(numbers_quadruple: Tuple[Real, Real, Real, Real]
                    ) -> None:
    (minuend_multiplier_x, minuend_multiplier_y,
     subtrahend_multiplier_x, subtrahend_multiplier_y) = numbers_quadruple

    result = to_cross_product(minuend_multiplier_x, minuend_multiplier_y,
                              subtrahend_multiplier_x, subtrahend_multiplier_y)

    assert is_sorted_by_magnitude_expansion(result)
    assert is_non_overlapping_expansion(result)
