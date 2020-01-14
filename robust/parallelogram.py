from numbers import Real

from . import bounds
from .hints import Point
from .utils import (X,
                    Y,
                    sum_expansions,
                    to_cross_product,
                    two_diff_tail,
                    two_product,
                    two_two_diff)


def signed_area(first_start: Point, first_end: Point,
                second_start: Point, second_end: Point) -> Real:
    """
    Calculates signed area of parallelogram built on segments' vectors.

    Positive sign of result means that second vector is counterclockwise,
    negative -- clockwise,
    zero -- collinear to first vector.
    """
    minuend = ((first_end[X] - first_start[X])
               * (second_end[Y] - second_start[Y]))
    subtrahend = ((first_end[Y] - first_start[Y])
                  * (second_end[X] - second_start[X]))
    result = minuend - subtrahend

    if minuend > 0:
        if subtrahend <= 0:
            return result
        else:
            upper_bound = minuend + subtrahend
    elif minuend < 0.0:
        if subtrahend >= 0.0:
            return result
        else:
            upper_bound = -minuend - subtrahend
    else:
        return result

    error_bound = bounds.to_signed_measure_first_error(upper_bound)
    if result >= error_bound or -result >= error_bound:
        return result

    return _adjusted_signed_area(first_start, first_end,
                                 second_start, second_end,
                                 upper_bound)


def _adjusted_signed_area(first_start: Point, first_end: Point,
                          second_start: Point, second_end: Point,
                          upper_bound: Real) -> Real:
    minuend_multiplier_x = first_end[X] - first_start[X]
    minuend_multiplier_y = second_end[Y] - second_start[Y]
    subtrahend_multiplier_x = second_end[X] - second_start[X]
    subtrahend_multiplier_y = first_end[Y] - first_start[Y]

    minuend_tail, minuend = two_product(minuend_multiplier_x,
                                        minuend_multiplier_y)
    subtrahend_tail, subtrahend = two_product(subtrahend_multiplier_y,
                                              subtrahend_multiplier_x)

    result_expansion = two_two_diff(minuend_tail, minuend, subtrahend_tail,
                                    subtrahend)
    result = sum(result_expansion)
    error_bound = bounds.to_signed_measure_second_error(upper_bound)
    if result >= error_bound or -result >= error_bound:
        return result

    minuend_multiplier_x_tail = two_diff_tail(first_end[X], first_start[X],
                                              minuend_multiplier_x)
    subtrahend_multiplier_x_tail = two_diff_tail(second_end[X],
                                                 second_start[X],
                                                 subtrahend_multiplier_x)
    subtrahend_multiplier_y_tail = two_diff_tail(first_end[Y], first_start[Y],
                                                 subtrahend_multiplier_y)
    minuend_multiplier_y_tail = two_diff_tail(second_end[Y], second_start[Y],
                                              minuend_multiplier_y)
    if (not minuend_multiplier_x_tail
            and not minuend_multiplier_y_tail
            and not subtrahend_multiplier_x_tail
            and not subtrahend_multiplier_y_tail):
        return result

    error_bound = (bounds.to_signed_measure_third_error(upper_bound)
                   + bounds.to_determinant_error(result))
    result += ((minuend_multiplier_x * minuend_multiplier_y_tail
                + minuend_multiplier_y * minuend_multiplier_x_tail)
               - (subtrahend_multiplier_y * subtrahend_multiplier_x_tail
                  + subtrahend_multiplier_x * subtrahend_multiplier_y_tail))
    if result >= error_bound or -result >= error_bound:
        return result

    result_expansion = sum_expansions(
            result_expansion, to_cross_product(minuend_multiplier_x_tail,
                                               minuend_multiplier_y,
                                               subtrahend_multiplier_x,
                                               subtrahend_multiplier_y_tail))
    result_expansion = sum_expansions(
            result_expansion, to_cross_product(minuend_multiplier_x,
                                               minuend_multiplier_y_tail,
                                               subtrahend_multiplier_x_tail,
                                               subtrahend_multiplier_y))
    result_expansion = sum_expansions(
            result_expansion, to_cross_product(minuend_multiplier_x_tail,
                                               minuend_multiplier_y_tail,
                                               subtrahend_multiplier_x_tail,
                                               subtrahend_multiplier_y_tail))
    return result_expansion[-1]
