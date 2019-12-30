from typing import Tuple

from hypothesis import given

from robust.hints import Scalar
from robust.utils import two_sum
from tests import strategies


@given(strategies.scalars_pairs)
def test_basic(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    result = two_sum(left, right)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(element, type(left)) for element in result)


@given(strategies.scalars_pairs)
def test_commutativity(scalars_pair: Tuple[Scalar, Scalar]) -> None:
    left, right = scalars_pair

    assert two_sum(left, right) == two_sum(right, left)
