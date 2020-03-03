from typing import Tuple

from hypothesis import given

from robust.angular import (Kind,
                            kind)
from robust.hints import Point
from tests.utils import equivalence
from . import strategies


@given(strategies.points_triplets)
def test_basic(points_triplet: Tuple[Point, Point, Point]) -> None:
    first_ray_point, vertex, second_ray_point = points_triplet

    result = kind(first_ray_point, vertex, second_ray_point)

    assert isinstance(result, Kind)


@given(strategies.points_pairs)
def test_same_endpoints(points_pair: Tuple[Point, Point]) -> None:
    start, end = points_pair

    assert equivalence(kind(start, end, start) is Kind.ACUTE,
                       start != end)
    assert equivalence(kind(start, end, start) is Kind.RIGHT,
                       start == end)


@given(strategies.points_triplets)
def test_endpoints_permutation(points_triplet: Tuple[Point, Point, Point]
                               ) -> None:
    first_ray_point, vertex, second_ray_point = points_triplet

    result = kind(first_ray_point, vertex, second_ray_point)

    assert result is kind(second_ray_point, vertex, first_ray_point)
