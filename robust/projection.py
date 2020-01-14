from numbers import Real

from . import parallelogram
from .hints import RealPoint
from .utils import to_perpendicular_point


def signed_length(first_start: RealPoint,
                  first_end: RealPoint,
                  second_start: RealPoint,
                  second_end: RealPoint) -> Real:
    """
    Calculates signed length of projection of one vector onto another.
    """
    return parallelogram.signed_area(first_start, first_end,
                                     to_perpendicular_point(second_start),
                                     to_perpendicular_point(second_end))
