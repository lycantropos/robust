from typing import Tuple

from hypothesis import given

from robust.hints import (Expansion,
                          Scalar)
from robust.utils import scale_expansion
from tests import strategies
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)


@given(strategies.expansions_with_scales)
def test_basic(expansion_with_scale: Tuple[Expansion, Scalar]) -> None:
    expansion, scale = expansion_with_scale

    result = scale_expansion(expansion, scale)

    assert isinstance(result, list)
    assert result
    assert all(isinstance(element, type(expansion[0]))
               for element in result)


@given(strategies.expansions_with_scales)
def test_properties(expansion_with_scale: Tuple[Expansion, Scalar]) -> None:
    expansion, scale = expansion_with_scale

    result = scale_expansion(expansion, scale)

    assert is_sorted_by_magnitude_expansion(result,
                                            zero_eliminated=True)
    assert is_non_overlapping_expansion(result)


@given(strategies.zero_expansions_with_scalars)
def test_left_absorbing_element(zero_expansion_with_scalar: Tuple[Expansion,
                                                                  Scalar]
                                ) -> None:
    zero_expansion, scalar = zero_expansion_with_scalar

    result = scale_expansion(zero_expansion, scalar)

    assert len(result) == 1
    assert all(not element for element in result)


@given(strategies.expansions_with_zeros)
def test_right_absorbing_element(expansion_with_zero: Expansion) -> None:
    expansion, zero = expansion_with_zero

    result = scale_expansion(expansion, zero)

    assert len(result) == 1
    assert all(not element for element in result)
