from typing import Tuple

from hypothesis import given

from robust.hints import Segment
from robust.linear import (SegmentsRelationship,
                           segments_intersections,
                           segments_relationship)
from tests.utils import (is_point,
                         reverse_point_coordinates,
                         reverse_segment,
                         reverse_segment_coordinates)
from . import strategies


@given(strategies.segments_pairs)
def test_basic(segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = segments_intersections(left_segment, right_segment)

    assert isinstance(result, tuple)
    assert all(is_point(element) for element in result)
    assert len(result) <= 2


@given(strategies.segments_pairs)
def test_commutativity(segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = segments_intersections(left_segment, right_segment)

    assert result == segments_intersections(right_segment, left_segment)


@given(strategies.segments)
def test_self(segment: Segment) -> None:
    result = segments_intersections(segment, segment)

    assert result == tuple(sorted(segment))


@given(strategies.segments_pairs)
def test_connection_with_segments_relationship(
        segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = segments_intersections(left_segment, right_segment)

    relationship = segments_relationship(left_segment, right_segment)
    assert (len(result)
            == (0 if relationship is SegmentsRelationship.NONE
                else (2 if relationship is SegmentsRelationship.OVERLAP
                      else 1)))


@given(strategies.segments)
def test_reversed(segment: Segment) -> None:
    result = segments_intersections(segment, reverse_segment(segment))

    assert result == tuple(sorted(segment))


@given(strategies.segments_pairs)
def test_reversed_coordinates(segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = segments_intersections(left_segment, right_segment)

    assert (tuple(sorted(map(reverse_point_coordinates, reversed(result))))
            == segments_intersections(
                    reverse_segment_coordinates(left_segment),
                    reverse_segment_coordinates(right_segment)))
