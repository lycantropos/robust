from itertools import permutations
from typing import Tuple

from hypothesis import given

from robust.cocircular import determinant
from robust.hints import Point
from tests.utils import (is_even_permutation,
                         permute,
                         to_sign)
from . import strategies


@given(strategies.points_quadruples)
def test_basic(points_quadruple: Tuple[Point, Point, Point, Point]) -> None:
    first_point, second_point, third_point, fourth_point = points_quadruple

    result = determinant(first_point, second_point, third_point, fourth_point)

    assert isinstance(result, type(first_point[0]))


@given(strategies.points_triplets)
def test_degenerate_cases(points_triplet: Tuple[Point, Point, Point]) -> None:
    first_point, second_point, third_point = points_triplet

    assert all(not determinant(first_point, second_point, third_point, point)
               for point in points_triplet)


@given(strategies.points_quadruples)
def test_permutations(points_quadruple: Tuple[Point, Point, Point, Point]
                      ) -> None:
    first_point, second_point, third_point, fourth_point = points_quadruple

    result = determinant(first_point, second_point, third_point, fourth_point)

    result_sign = to_sign(result)
    assert all(to_sign(determinant(*permute(points_quadruple, permutation)))
               == (result_sign
                   if is_even_permutation(permutation)
                   else -result_sign)
               for permutation in permutations(range(len(points_quadruple))))
