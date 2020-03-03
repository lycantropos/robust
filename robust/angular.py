from enum import (IntEnum,
                  unique)
from numbers import Real

from .hints import Point
from .parallelogram import signed_area
from .projection import signed_length


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
    return Kind(_to_sign(signed_length(vertex, first_ray_point,
                                       vertex, second_ray_point)))


def orientation(first_ray_point: Point,
                vertex: Point,
                second_ray_point: Point) -> Orientation:
    return Orientation(_to_sign(signed_area(vertex, first_ray_point,
                                            vertex, second_ray_point)))


def _to_sign(value: Real) -> int:
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0
