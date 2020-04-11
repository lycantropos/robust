from enum import (IntEnum,
                  unique)

from .hints import Point
from .parallelogram import signed_area
from .projection import signed_length
from .utils import to_sign


@unique
class Kind(IntEnum):
    """
    Represents kinds of angles
    based on their degrees value in range ``[0, 180]``.
    """
    #: ``(90, 180]`` degrees
    OBTUSE = -1
    #: ``90`` degrees
    RIGHT = 0
    #: ``[0, 90)`` degrees
    ACUTE = 1


@unique
class Orientation(IntEnum):
    """
    Represents kinds of angle orientations.
    """
    #: in the same direction as a clock's hands
    CLOCKWISE = -1
    #: to the top and then to the bottom or vice versa
    COLLINEAR = 0
    #: opposite to clockwise
    COUNTERCLOCKWISE = 1


def kind(first_ray_point: Point,
         vertex: Point,
         second_ray_point: Point) -> Kind:
    """
    Returns kind of angle built on given points.

    >>> kind((1, 0), (0, 0), (1, 0)) is Kind.ACUTE
    True
    >>> kind((1, 0), (0, 0), (0, 1)) is Kind.RIGHT
    True
    >>> kind((1, 0), (0, 0), (-1, 0)) is Kind.OBTUSE
    True
    """
    return Kind(to_sign(signed_length(vertex, first_ray_point,
                                      vertex, second_ray_point)))


def orientation(first_ray_point: Point,
                vertex: Point,
                second_ray_point: Point) -> Orientation:
    """
    Returns orientation of angle built on given points.

    >>> orientation((1, 0), (0, 0), (1, 0)) is Orientation.COLLINEAR
    True
    >>> orientation((1, 0), (0, 0), (0, 1)) is Orientation.COUNTERCLOCKWISE
    True
    >>> orientation((0, 1), (0, 0), (1, 0)) is Orientation.CLOCKWISE
    True
    """
    return Orientation(to_sign(signed_area(vertex, first_ray_point,
                                           vertex, second_ray_point)))
