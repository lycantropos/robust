from itertools import permutations
from typing import Tuple

from hypothesis import given

from robust.angular import (Orientation,
                            orientation)
from robust.hints import Point
from tests.utils import (is_even_permutation,
                         permute)
from . import strategies


@given(strategies.points_triplets)
def test_basic(points_triplet: Tuple[Point, Point, Point]) -> None:
    first_ray_point, vertex, second_ray_point = points_triplet

    result = orientation(first_ray_point, vertex, second_ray_point)

    assert isinstance(result, Orientation)


@given(strategies.points_pairs)
def test_same_endpoints(points_pair: Tuple[Point, Point]) -> None:
    start, end = points_pair

    assert (orientation(start, end, start)
            is Orientation.COLLINEAR)
    assert (orientation(start, end, end)
            is Orientation.COLLINEAR)


@given(strategies.points_triplets)
def test_permutations(points_triplet: Tuple[Point, Point, Point]) -> None:
    first_start, first_end, second_start = points_triplet

    result = orientation(first_start, first_end, second_start)

    assert all(orientation(*permute(points_triplet, permutation))
               is (result
                   if is_even_permutation(permutation)
                   else Orientation(-result))
               for permutation in permutations(range(len(points_triplet))))
