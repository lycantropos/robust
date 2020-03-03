from enum import (IntEnum,
                  unique)
from fractions import Fraction
from typing import (Tuple,
                    Union)

from .angular import (Kind,
                      Orientation,
                      kind,
                      orientation)
from .hints import (Point,
                    Segment)
from .parallelogram import signed_area


@unique
class SegmentsRelationship(IntEnum):
    NONE = 0
    CROSS = 1
    OVERLAP = 2


def segments_relationship(left: Segment,
                          right: Segment) -> SegmentsRelationship:
    if left == right or left == right[::-1]:
        return SegmentsRelationship.OVERLAP
    left_start, left_end = left
    right_start, right_end = right
    left_start_orientation = orientation(right_start, right_end, left_start, )
    left_end_orientation = orientation(right_start, right_end, left_end)
    if (left_start_orientation is Orientation.COLLINEAR
            and _bounding_box_contains(right, left_start)):
        if left_end_orientation is Orientation.COLLINEAR:
            if left_start == right_start:
                if kind(left_end, left_start, right_end) is Kind.ACUTE:
                    return SegmentsRelationship.OVERLAP
                else:
                    return SegmentsRelationship.CROSS
            elif left_start == right_end:
                if kind(left_end, left_start, right_start) is Kind.ACUTE:
                    return SegmentsRelationship.OVERLAP
                else:
                    return SegmentsRelationship.CROSS
            else:
                return SegmentsRelationship.OVERLAP
        else:
            return SegmentsRelationship.CROSS
    elif (left_end_orientation is Orientation.COLLINEAR
          and _bounding_box_contains(right, left_end)):
        if left_start_orientation is Orientation.COLLINEAR:
            if left_end == right_start:
                if kind(left_start, left_end, right_end) is Kind.ACUTE:
                    return SegmentsRelationship.OVERLAP
                else:
                    return SegmentsRelationship.CROSS
            elif left_end == right_end:
                if kind(left_start, left_end, right_start) is Kind.ACUTE:
                    return SegmentsRelationship.OVERLAP
                else:
                    return SegmentsRelationship.CROSS
            else:
                return SegmentsRelationship.OVERLAP
        else:
            return SegmentsRelationship.CROSS
    else:
        right_start_orientation = orientation(left_end, left_start,
                                              right_start)
        right_end_orientation = orientation(left_end, left_start, right_end)
        if (left_start_orientation * left_end_orientation < 0
                and right_start_orientation * right_end_orientation < 0):
            return SegmentsRelationship.CROSS
        elif (right_start_orientation is Orientation.COLLINEAR
              and _bounding_box_contains(left, right_start)):
            return (SegmentsRelationship.OVERLAP
                    if right_end_orientation is Orientation.COLLINEAR
                    else SegmentsRelationship.CROSS)
        elif (right_end_orientation is Orientation.COLLINEAR
              and _bounding_box_contains(left, right_end)):
            return (SegmentsRelationship.OVERLAP
                    if right_start_orientation is Orientation.COLLINEAR
                    else SegmentsRelationship.CROSS)
        else:
            return SegmentsRelationship.NONE


def segments_intersections(left: Segment,
                           right: Segment) -> Union[Tuple[()], Tuple[Point],
                                                    Tuple[Point, Point]]:
    relationship = segments_relationship(left, right)
    if relationship is SegmentsRelationship.NONE:
        return ()
    elif relationship is SegmentsRelationship.CROSS:
        return segments_intersection(left, right),
    else:
        _, first_intersection, second_intersection, _ = sorted(left + right)
        return first_intersection, second_intersection


def segments_intersection(left: Segment, right: Segment) -> Point:
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
        base_numerators_diff = (abs(right_base_numerator)
                                - abs(left_base_numerator))
        denominator_inv = (Fraction(1, denominator)
                           if isinstance(denominator, int)
                           else 1 / denominator)
        if not base_numerators_diff:
            left_start_x, left_start_y = left_start
            left_end_x, left_end_y = left_end
            right_start_x, right_start_y = right_start
            right_end_x, right_end_y = right_end
            return ((left_start_x + right_start_x
                     + ((left_end_x - left_start_x) * left_base_numerator
                        + (right_end_x - right_start_x) * right_base_numerator)
                     * denominator_inv) / 2,
                    (left_start_y + right_start_y
                     + ((left_end_y - left_start_y) * left_base_numerator
                        + (right_end_y - right_start_y) * right_base_numerator)
                     * denominator_inv) / 2)
        elif base_numerators_diff > 0:
            left_start_x, left_start_y = left_start
            left_end_x, left_end_y = left_end
            return (left_start_x
                    + left_base_numerator * (left_end_x - left_start_x)
                    * denominator_inv,
                    left_start_y
                    + left_base_numerator * (left_end_y - left_start_y)
                    * denominator_inv)
        else:
            right_start_x, right_start_y = right_start
            right_end_x, right_end_y = right_end
            return (right_start_x
                    + right_base_numerator * (right_end_x - right_start_x)
                    * denominator_inv,
                    right_start_y
                    + right_base_numerator * (right_end_y - right_start_y)
                    * denominator_inv)


def segment_contains(segment: Segment, point: Point) -> bool:
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
