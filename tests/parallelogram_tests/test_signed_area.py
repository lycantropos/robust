from itertools import permutations, product
from typing import Tuple

from hypothesis import given

from robust.hints import Point
from robust.parallelogram import signed_area
from tests.utils import (equivalence, is_even_permutation, permute, to_sign)
from . import strategies


@given(strategies.points_quadruples)
def test_basic(points_quadruple: Tuple[Point, Point, Point, Point]) -> None:
    first_start, first_end, second_start, second_end = points_quadruple

    result = signed_area(first_start, first_end, second_start, second_end)

    assert isinstance(result, type(first_start[0]))


@given(strategies.points_pairs)
def test_same_endpoints(points_pair: Tuple[Point, Point]) -> None:
    first_start, first_end = points_pair

    assert not signed_area(first_start, first_end, first_start, first_end)


@given(strategies.points_quadruples)
def test_segments_permutation(points_quadruple: Tuple[Point, Point,
                                                      Point, Point]) -> None:
    first_start, first_end, second_start, second_end = points_quadruple

    result = signed_area(first_start, first_end, second_start, second_end)

    assert result == -signed_area(second_start, second_end,
                                  first_start, first_end)


@given(strategies.points_quadruples)
def test_endpoints_permutations(points_quadruple: Tuple[Point, Point,
                                                        Point, Point]) -> None:
    first_start, first_end, second_start, second_end = points_quadruple

    result = signed_area(first_start, first_end, second_start, second_end)

    result_sign = to_sign(result)
    first_endpoints = first_start, first_end
    second_endpoints = second_start, second_end
    assert all(
            to_sign(signed_area(*permute(first_endpoints,
                                         first_permutation),
                                *permute(second_endpoints,
                                         second_permutation)))
            == (result_sign
                if equivalence(is_even_permutation(first_permutation),
                               is_even_permutation(second_permutation))
                else -result_sign)
            for first_permutation, second_permutation in product(
                    permutations(range(len(first_endpoints))),
                    permutations(range(len(second_endpoints)))))
