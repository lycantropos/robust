from typing import Tuple

from hypothesis import given

from robust.hints import Segment
from robust.linear import (find_intersections,
                           segments_relationship)
from tests.utils import (is_point,
                         reverse_segment)
from . import strategies


@given(strategies.segments_pairs)
def test_basic(segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = find_intersections(left_segment, right_segment)

    assert isinstance(result, tuple)
    assert all(is_point(element) for element in result)
    assert len(result) <= 2


@given(strategies.segments_pairs)
def test_commutativity(segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = find_intersections(left_segment, right_segment)

    assert result == find_intersections(right_segment, left_segment)


@given(strategies.segments)
def test_self(segment: Segment) -> None:
    result = find_intersections(segment, segment)

    assert result == tuple(sorted(segment))


@given(strategies.segments_pairs)
def test_connection_with_segments_relationship(
        segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = find_intersections(left_segment, right_segment)

    assert len(result) == segments_relationship(left_segment, right_segment)


@given(strategies.segments)
def test_reversed(segment: Segment) -> None:
    result = find_intersections(segment, reverse_segment(segment))

    assert result == tuple(sorted(segment))
