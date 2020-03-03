from enum import (IntEnum,
                  unique)

from .hints import Point
from .parallelogram import signed_area
from .projection import signed_length
from .utils import to_sign


@unique
class Kind(IntEnum):
    OBTUSE = -1
    RIGHT = 0
    ACUTE = 1


@unique
class Orientation(IntEnum):
    CLOCKWISE = -1
    COLLINEAR = 0
    COUNTERCLOCKWISE = 1


def kind(first_ray_point: Point,
         vertex: Point,
         second_ray_point: Point) -> Kind:
    """
    Returns kind of angle built on given points.

    >>> kind((1, 0), (0, 0), (1, 0)) is Kind.ACUTE
    >>> kind((1, 0), (0, 0), (0, 1)) is Kind.RIGHT
    >>> kind((1, 0), (0, 0), (-1, 0)) is Kind.OBTUSE
    """
    return Kind(to_sign(signed_length(vertex, first_ray_point,
                                      vertex, second_ray_point)))


def orientation(first_ray_point: Point,
                vertex: Point,
                second_ray_point: Point) -> Orientation:
    """
    Returns orientation of angle built on given points.

    >>> orientation((1, 0), (0, 0), (1, 0)) is Orientation.COLLINEAR
    >>> orientation((1, 0), (0, 0), (0, 1)) is Orientation.COUNTERCLOCKWISE
    >>> orientation((0, 1), (0, 0), (1, 0)) is Orientation.CLOCKWISE
    """
    return Orientation(to_sign(signed_area(vertex, first_ray_point,
                                           vertex, second_ray_point)))
