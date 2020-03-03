from typing import Tuple

from hypothesis import given

from robust.linear import (Segment,
                           SegmentsRelationship,
                           segments_relationship)
from tests.utils import (reflect_segment,
                         reverse_segment)
from . import strategies


@given(strategies.segments_pairs)
def test_basic(segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = segments_relationship(left_segment, right_segment)

    assert isinstance(result, SegmentsRelationship)


@given(strategies.segments_pairs)
def test_commutativity(segments_pair: Tuple[Segment, Segment]) -> None:
    left_segment, right_segment = segments_pair

    result = segments_relationship(left_segment, right_segment)

    assert result is segments_relationship(right_segment, left_segment)


@given(strategies.segments)
def test_self(segment: Segment) -> None:
    result = segments_relationship(segment, segment)

    assert result is SegmentsRelationship.OVERLAP


@given(strategies.segments)
def test_reversed(segment: Segment) -> None:
    result = segments_relationship(segment, reverse_segment(segment))

    assert result is SegmentsRelationship.OVERLAP


@given(strategies.segments)
def test_reflected(segment: Segment) -> None:
    result = segments_relationship(segment, reflect_segment(segment))

    assert result is SegmentsRelationship.CROSS
