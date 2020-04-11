from numbers import Real

from . import parallelogram
from .hints import Point
from .utils import to_perpendicular_point


def signed_length(first_start: Point, first_end: Point,
                  second_start: Point, second_end: Point) -> Real:
    """
    Calculates signed length of projection of one vector onto another.

    Positive sign of result means that angle between vectors is acute,
    negative -- obtuse,
    zero -- right.

    >>> signed_length((0, 0), (1, 0), (0, 0), (1, 0))
    1
    >>> signed_length((0, 0), (1, 0), (0, 0), (0, 1))
    0
    >>> signed_length((0, 0), (1, 0), (1, 0), (0, 0))
    -1
    """
    return parallelogram.signed_area(first_start, first_end,
                                     to_perpendicular_point(second_start),
                                     to_perpendicular_point(second_end))
