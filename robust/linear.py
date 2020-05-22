from enum import (IntEnum,
                  unique)
from fractions import Fraction
from typing import Tuple

from .angular import (Orientation,
                      orientation)
from .hints import (Point,
                    Segment)
from .parallelogram import signed_area


@unique
class SegmentsRelationship(IntEnum):
    """
    Represents relationship between segments based on their intersection.
    """
    #: intersection is empty
    NONE = 0
    #: intersection is an endpoint of one of segments
    TOUCH = 1
    #: intersection is a point which is not an endpoint of any of segments
    CROSS = 2
    #: intersection is a segment itself
    OVERLAP = 3


def segments_relationship(left: Segment,
                          right: Segment) -> SegmentsRelationship:
    """
    Finds relationship between segments.

    >>> (segments_relationship(((0, 0), (2, 0)), ((0, 0), (2, 0)))
    ...  is SegmentsRelationship.OVERLAP)
    True
    >>> (segments_relationship(((0, 0), (2, 0)), ((0, 0), (0, 2)))
    ...  is SegmentsRelationship.TOUCH)
    True
    >>> (segments_relationship(((0, 0), (2, 0)), ((0, 0), (1, 0)))
    ...  is SegmentsRelationship.OVERLAP)
    True
    >>> (segments_relationship(((0, 0), (2, 0)), ((1, 0), (1, 1)))
    ...  is SegmentsRelationship.TOUCH)
    True
    >>> (segments_relationship(((0, 0), (2, 0)), ((1, 0), (2, 0)))
    ...  is SegmentsRelationship.OVERLAP)
    True
    >>> (segments_relationship(((0, 0), (2, 0)), ((2, 0), (3, 0)))
    ...  is SegmentsRelationship.TOUCH)
    True
    >>> (segments_relationship(((0, 0), (2, 0)), ((3, 0), (4, 0)))
    ...  is SegmentsRelationship.NONE)
    True
    """
    if left == right or left == right[::-1]:
        return SegmentsRelationship.OVERLAP
    left_start, left_end = left
    right_start, right_end = right
    if left_start > left_end:
        left_start, left_end = left_end, left_start
    if right_start > right_end:
        right_start, right_end = right_end, right_start
    left_start_orientation = orientation(right_start, right_end, left_start)
    left_end_orientation = orientation(right_start, right_end, left_end)
    if left_start_orientation is left_end_orientation:
        if left_start_orientation is Orientation.COLLINEAR:
            if left_start == right_start:
                return SegmentsRelationship.OVERLAP
            elif left_end == right_end:
                return SegmentsRelationship.OVERLAP
            elif left_start == right_end or left_end == right_start:
                return SegmentsRelationship.TOUCH
            elif right_start < left_start < right_end:
                return SegmentsRelationship.OVERLAP
            elif left_start < right_start < left_end:
                return SegmentsRelationship.OVERLAP
            else:
                return SegmentsRelationship.NONE
        else:
            return SegmentsRelationship.NONE
    elif left_start_orientation is Orientation.COLLINEAR:
        return (SegmentsRelationship.TOUCH
                if right_start <= left_start <= right_end
                else SegmentsRelationship.NONE)
    elif left_end_orientation is Orientation.COLLINEAR:
        return (SegmentsRelationship.TOUCH
                if right_start <= left_end <= right_end
                else SegmentsRelationship.NONE)
    else:
        right_start_orientation = orientation(left_end, left_start,
                                              right_start)
        right_end_orientation = orientation(left_end, left_start, right_end)
        if right_start_orientation is right_end_orientation:
            return SegmentsRelationship.NONE
        elif right_start_orientation is Orientation.COLLINEAR:
            return (SegmentsRelationship.TOUCH
                    if left_start < right_start < left_end
                    else SegmentsRelationship.NONE)
        elif right_end_orientation is Orientation.COLLINEAR:
            return (SegmentsRelationship.TOUCH
                    if left_start < right_end < left_end
                    else SegmentsRelationship.NONE)
        else:
            return SegmentsRelationship.CROSS


def segments_intersections(left: Segment, right: Segment) -> Tuple[Point, ...]:
    """
    Finds intersections of segments.

    >>> (segments_intersections(((0, 0), (2, 0)), ((0, 0), (2, 0)))
    ...  == ((0, 0), (2, 0)))
    True
    >>> segments_intersections(((0, 0), (2, 0)), ((0, 0), (0, 2))) == ((0, 0),)
    True
    >>> (segments_intersections(((0, 0), (2, 0)), ((0, 0), (1, 0)))
    ...  == ((0, 0), (1, 0)))
    True
    >>> segments_intersections(((0, 0), (2, 0)), ((1, 0), (1, 1))) == ((1, 0),)
    True
    >>> (segments_intersections(((0, 0), (2, 0)), ((1, 0), (2, 0)))
    ...  == ((1, 0), (2, 0)))
    True
    >>> segments_intersections(((0, 0), (2, 0)), ((2, 0), (3, 0))) == ((2, 0),)
    True
    >>> segments_intersections(((0, 0), (2, 0)), ((3, 0), (4, 0))) == ()
    True
    """
    relationship = segments_relationship(left, right)
    if relationship is SegmentsRelationship.NONE:
        return ()
    elif relationship is SegmentsRelationship.OVERLAP:
        _, first_intersection, second_intersection, _ = sorted(left + right)
        return first_intersection, second_intersection
    else:
        return segments_intersection(left, right),


def segments_intersection(left: Segment, right: Segment) -> Point:
    """
    Finds intersection point of segments that known to have only one.

    >>> segments_intersection(((0, 0), (2, 0)), ((0, 0), (0, 2))) == (0, 0)
    True
    >>> segments_intersection(((0, 0), (2, 0)), ((1, 0), (1, 1))) == (1, 0)
    True
    >>> segments_intersection(((0, 0), (2, 0)), ((2, 0), (3, 0))) == (2, 0)
    True
    """
    left_start, left_end = left
    right_start, right_end = right
    if segment_contains(left, right_start):
        return right_start
    elif segment_contains(left, right_end):
        return right_end
    elif segment_contains(right, left_start):
        return left_start
    elif segment_contains(right, left_end):
        return left_end
    else:
        denominator = signed_area(left_start, left_end, right_start, right_end)
        left_base_numerator = signed_area(left_start, right_start,
                                          right_start, right_end)
        right_base_numerator = signed_area(left_start, right_start,
                                           left_start, left_end)
        left_start_x, left_start_y = left_start
        left_end_x, left_end_y = left_end
        right_start_x, right_start_y = right_start
        right_end_x, right_end_y = right_end
        left_x_addend = (left_end_x - left_start_x) * left_base_numerator
        left_y_addend = (left_end_y - left_start_y) * left_base_numerator
        right_x_addend = (right_end_x - right_start_x) * right_base_numerator
        right_y_addend = (right_end_y - right_start_y) * right_base_numerator
        delta_x, delta_y = (abs(right_x_addend) - abs(left_x_addend),
                            abs(right_y_addend) - abs(left_y_addend))
        denominator_inv = (Fraction(1, denominator)
                           if isinstance(denominator, int)
                           else 1 / denominator)
        return (left_start_x + left_x_addend * denominator_inv
                if delta_x > 0
                else (right_start_x + right_x_addend * denominator_inv
                      if delta_x < 0
                      else (left_start_x + right_start_x
                            + (left_x_addend + right_x_addend)
                            * denominator_inv) / 2),
                left_start_y + left_y_addend * denominator_inv
                if delta_y > 0
                else (right_start_y + right_y_addend * denominator_inv
                      if delta_y < 0
                      else (left_start_y + right_start_y
                            + (left_y_addend + right_y_addend)
                            * denominator_inv) / 2))


def segment_contains(segment: Segment, point: Point) -> bool:
    """
    Checks if segment contains point.

    >>> segment_contains(((0, 0), (2, 0)), (0, 0))
    True
    >>> segment_contains(((0, 0), (2, 0)), (0, 2))
    False
    >>> segment_contains(((0, 0), (2, 0)), (1, 0))
    True
    >>> segment_contains(((0, 0), (2, 0)), (1, 1))
    False
    >>> segment_contains(((0, 0), (2, 0)), (2, 0))
    True
    >>> segment_contains(((0, 0), (2, 0)), (3, 0))
    False
    """
    start, end = segment
    return (point == start or point == end
            or (_bounding_box_contains(segment, point)
                and orientation(end, start, point) is Orientation.COLLINEAR))


def _bounding_box_contains(segment: Segment, point: Point) -> bool:
    (start_x, start_y), (end_x, end_y) = segment
    left_x, right_x = ((start_x, end_x)
                       if start_x < end_x
                       else (end_x, start_x))
    bottom_y, top_y = ((start_y, end_y)
                       if start_y < end_y
                       else (end_y, start_y))
    point_x, point_y = point
    return left_x <= point_x <= right_x and bottom_y <= point_y <= top_y
