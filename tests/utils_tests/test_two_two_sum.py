from typing import Tuple

from hypothesis import given

from robust.hints import Scalar
from robust.utils import (two_sum,
                          two_two_sum)
from tests import strategies
from tests.utils import (is_non_overlapping_expansion,
                         is_sorted_by_magnitude_expansion)


@given(strategies.non_overlapping_scalars_pairs_pairs)
def test_basic(scalars_pairs_pair: Tuple[Tuple[Scalar, Scalar],
                                         Tuple[Scalar, Scalar]]) -> None:
    (left_tail, left), (right_tail, right) = scalars_pairs_pair

    result = two_two_sum(left_tail, left, right_tail, right)

    assert isinstance(result, tuple)
    assert len(result) == 4
    assert all(isinstance(element, type(left)) for element in result)


@given(strategies.non_overlapping_scalars_pairs_pairs)
def test_properties(scalars_pairs_pair: Tuple[Tuple[Scalar, Scalar],
                                              Tuple[Scalar, Scalar]]) -> None:
    (left_tail, left), (right_tail, right) = scalars_pairs_pair

    result = two_two_sum(left_tail, left, right_tail, right)

    assert is_sorted_by_magnitude_expansion(result)
    assert is_non_overlapping_expansion(result)


@given(strategies.non_overlapping_scalars_pairs)
def test_left_neutral_element(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    scalar_tail, scalar = scalars_pair

    assert (two_two_sum(0, 0, scalar_tail, scalar)
            == (0, 0, *two_sum(scalar_tail, scalar)))


@given(strategies.non_overlapping_scalars_pairs)
def test_right_neutral_element(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    scalar_tail, scalar = scalars_pair

    assert (two_two_sum(scalar_tail, scalar, 0, 0)
            == (0, 0, *two_sum(scalar_tail, scalar)))
