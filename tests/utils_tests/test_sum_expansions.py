from typing import Tuple

from hypothesis import given

from robust.hints import Expansion
from robust.utils import sum_expansions
from tests import strategies
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)


@given(strategies.expansions_pairs)
def test_basic(expansions_pair: Tuple[Expansion, Expansion]) -> None:
    left_expansion, right_expansion = expansions_pair

    result = sum_expansions(left_expansion, right_expansion)

    assert isinstance(result, list)
    assert result
    assert all(isinstance(element, type(left_expansion[0]))
               for element in result)


@given(strategies.expansions_pairs)
def test_properties(expansions_pair: Tuple[Expansion, Expansion]) -> None:
    left_expansion, right_expansion = expansions_pair

    result = sum_expansions(left_expansion, right_expansion)

    assert is_sorted_by_magnitude_expansion(result,
                                            zero_eliminated=True)
    assert is_non_overlapping_expansion(result)
