from functools import reduce
from numbers import Real
from typing import (Iterable,
                    Tuple)

from . import bounds
from .hints import (Expansion,
                    Point)
from .utils import (scale_expansion,
                    square,
                    sum_expansions,
                    to_cross_product,
                    two_diff_tail,
                    two_product,
                    two_two_diff,
                    two_two_sum)


def determinant(first_point: Point,
                second_point: Point,
                third_point: Point,
                fourth_point: Point) -> Real:
    """
    Calculates determinant of linear equations' system
    for checking if four points lie on the same circle.

    Positive sign of result means that point lies inside,
    negative -- outside,
    zero -- on a circle defined by other points.

    >>> determinant((0, 0), (2, 0), (2, 2), (0, 2))
    0
    >>> determinant((0, 0), (2, 0), (2, 2), (0, 3))
    -12
    >>> determinant((0, 0), (2, 0), (2, 2), (0, 1))
    4
    """
    first_x, first_y = first_point
    second_x, second_y = second_point
    third_x, third_y = third_point
    fourth_x, fourth_y = fourth_point
    first_dx, first_dy = first_x - fourth_x, first_y - fourth_y
    second_dx, second_dy = second_x - fourth_x, second_y - fourth_y
    third_dx, third_dy = third_x - fourth_x, third_y - fourth_y
    first_squared_distance = first_dx * first_dx + first_dy * first_dy
    second_squared_distance = second_dx * second_dx + second_dy * second_dy
    third_squared_distance = third_dx * third_dx + third_dy * third_dy
    first_dx_second_dy = first_dx * second_dy
    first_dx_third_dy = first_dx * third_dy
    second_dx_first_dy = second_dx * first_dy
    second_dx_third_dy = second_dx * third_dy
    third_dx_first_dy = third_dx * first_dy
    third_dx_second_dy = third_dx * second_dy
    result = (first_squared_distance
              * (second_dx_third_dy - third_dx_second_dy)
              + second_squared_distance
              * (third_dx_first_dy - first_dx_third_dy)
              + third_squared_distance
              * (first_dx_second_dy - second_dx_first_dy))
    upper_bound = (first_squared_distance
                   * (abs(second_dx_third_dy) + abs(third_dx_second_dy))
                   + second_squared_distance
                   * (abs(third_dx_first_dy) + abs(first_dx_third_dy))
                   + third_squared_distance
                   * (abs(first_dx_second_dy) + abs(second_dx_first_dy)))
    error_bound = bounds.to_cocircular_first_error(upper_bound)
    if result > error_bound or -result > error_bound:
        return result
    return _adjusted_determinant(first_x, first_y, second_x, second_y, third_x,
                                 third_y, fourth_x, fourth_y, upper_bound)


def _adjusted_determinant(first_x: Real,
                          first_y: Real,
                          second_x: Real,
                          second_y: Real,
                          third_x: Real,
                          third_y: Real,
                          fourth_x: Real,
                          fourth_y: Real,
                          upper_bound: Real) -> Real:
    first_dx_head, first_dy_head = first_x - fourth_x, first_y - fourth_y
    second_dx_head, second_dy_head = second_x - fourth_x, second_y - fourth_y
    third_dx_head, third_dy_head = third_x - fourth_x, third_y - fourth_y
    second_third_cross_product = to_cross_product(second_dx_head,
                                                  third_dy_head, third_dx_head,
                                                  second_dy_head)
    third_first_cross_product = to_cross_product(third_dx_head, first_dy_head,
                                                 first_dx_head, third_dy_head)
    first_second_cross_product = to_cross_product(first_dx_head,
                                                  second_dy_head,
                                                  second_dx_head,
                                                  first_dy_head)
    result_expansion = sum_expansions(
            sum_expansions(
                    _multiply_by_squared_length(second_third_cross_product,
                                                first_dx_head, first_dy_head),
                    _multiply_by_squared_length(third_first_cross_product,
                                                second_dx_head,
                                                second_dy_head)),
            _multiply_by_squared_length(first_second_cross_product,
                                        third_dx_head, third_dy_head))
    result = sum(result_expansion)
    error_bound = bounds.to_cocircular_second_error(upper_bound)
    if result >= error_bound or -result >= error_bound:
        return result
    first_dx_tail = two_diff_tail(first_x, fourth_x, first_dx_head)
    first_dy_tail = two_diff_tail(first_y, fourth_y, first_dy_head)
    second_dx_tail = two_diff_tail(second_x, fourth_x, second_dx_head)
    second_dy_tail = two_diff_tail(second_y, fourth_y, second_dy_head)
    third_dx_tail = two_diff_tail(third_x, fourth_x, third_dx_head)
    third_dy_tail = two_diff_tail(third_y, fourth_y, third_dy_head)
    if (not first_dx_tail and not first_dy_tail
            and not second_dx_tail and not second_dy_tail
            and not third_dx_tail and not third_dy_tail):
        return result
    error_bound = (bounds.to_cocircular_third_error(upper_bound)
                   + bounds.to_determinant_error(result))
    result += (_to_addend(first_dx_head, first_dx_tail, first_dy_head,
                          first_dy_tail, second_dx_head, second_dx_tail,
                          second_dy_head, second_dy_tail, third_dx_head,
                          third_dx_tail, third_dy_head, third_dy_tail)
               + _to_addend(second_dx_head, second_dx_tail, second_dy_head,
                            second_dy_tail, third_dx_head, third_dx_tail,
                            third_dy_head, third_dy_tail, first_dx_head,
                            first_dx_tail, first_dy_head, first_dy_tail)
               + _to_addend(third_dx_head, third_dx_tail, third_dy_head,
                            third_dy_tail, first_dx_head, first_dx_tail,
                            first_dy_head, first_dy_tail, second_dx_head,
                            second_dx_tail, second_dy_head, second_dy_tail))
    if result >= error_bound or -result >= error_bound:
        return result
    first_squared_length = (_to_squared_length(first_dx_head, first_dy_head)
                            if (second_dx_tail or second_dy_tail
                                or third_dx_tail or third_dy_tail)
                            else (0,) * 4)
    second_squared_length = (_to_squared_length(second_dx_head, second_dy_head)
                             if (first_dx_tail or first_dy_tail
                                 or third_dx_tail or third_dy_tail)
                             else (0,) * 4)
    third_squared_length = (_to_squared_length(third_dx_head, third_dy_head)
                            if (first_dx_tail or first_dy_tail
                                or second_dx_tail or second_dy_tail)
                            else (0,) * 4)
    if first_dx_tail:
        first_dx_tail_second_third_cross_product = scale_expansion(
                second_third_cross_product, first_dx_tail)
        result_expansion = sum_expansions(
                result_expansion,
                _to_extra(first_dx_tail_second_third_cross_product,
                          first_dx_head, first_dx_tail, second_dy_head,
                          second_squared_length, third_dy_head,
                          third_squared_length))
    if first_dy_tail:
        first_dy_tail_second_third_cross_product = scale_expansion(
                second_third_cross_product, first_dy_tail)
        result_expansion = sum_expansions(
                result_expansion,
                _to_extra(first_dy_tail_second_third_cross_product,
                          first_dy_head, first_dy_tail, third_dx_head,
                          third_squared_length, second_dx_head,
                          second_squared_length))
    if second_dx_tail:
        second_dx_tail_third_first_cross_product = scale_expansion(
                third_first_cross_product, second_dx_tail)
        result_expansion = sum_expansions(
                result_expansion,
                _to_extra(second_dx_tail_third_first_cross_product,
                          second_dx_head, second_dx_tail, third_dy_head,
                          third_squared_length, first_dy_head,
                          first_squared_length))
    if second_dy_tail:
        second_dy_tail_third_first_cross_product = scale_expansion(
                third_first_cross_product, second_dy_tail)
        result_expansion = sum_expansions(
                result_expansion,
                _to_extra(second_dy_tail_third_first_cross_product,
                          second_dy_head, second_dy_tail,
                          first_dx_head, first_squared_length,
                          third_dx_head, third_squared_length))
    if third_dx_tail:
        third_dx_tail_first_second_cross_product = scale_expansion(
                first_second_cross_product, third_dx_tail)
        result_expansion = sum_expansions(
                result_expansion,
                _to_extra(third_dx_tail_first_second_cross_product,
                          third_dx_head, third_dx_tail, first_dy_head,
                          first_squared_length, second_dy_head,
                          second_squared_length))
    if third_dy_tail:
        third_dy_tail_first_second_cross_product = scale_expansion(
                first_second_cross_product, third_dy_tail)
        result_expansion = sum_expansions(
                result_expansion,
                _to_extra(third_dy_tail_first_second_cross_product,
                          third_dy_head, third_dy_tail, second_dx_head,
                          second_squared_length, first_dx_head,
                          first_squared_length))
    if first_dx_tail or first_dy_tail:
        if second_dx_tail or second_dy_tail or third_dx_tail or third_dy_tail:
            second_third_crossed_tails_tail, second_third_crossed_tails = (
                _to_crossed_tails(second_dx_head, second_dx_tail,
                                  second_dy_head, second_dy_tail,
                                  third_dx_head, third_dx_tail, third_dy_head,
                                  third_dy_tail))
        else:
            second_third_crossed_tails_tail = second_third_crossed_tails = (0,)
        if first_dx_tail:
            result_expansion = reduce(
                    sum_expansions,
                    _to_dx_extras(first_dx_tail_second_third_cross_product,
                                  first_dx_head, first_dx_tail, second_dy_tail,
                                  second_squared_length, third_dy_tail,
                                  third_squared_length,
                                  second_third_crossed_tails,
                                  second_third_crossed_tails_tail),
                    result_expansion)
        if first_dy_tail:
            result_expansion = reduce(
                    sum_expansions,
                    _to_dy_extras(first_dy_tail_second_third_cross_product,
                                  first_dy_head, first_dy_tail,
                                  second_third_crossed_tails,
                                  second_third_crossed_tails_tail),
                    result_expansion)
    if second_dx_tail or second_dy_tail:
        if first_dx_tail or first_dy_tail or third_dx_tail or third_dy_tail:
            third_first_crossed_tails_tail, third_first_crossed_tails = (
                _to_crossed_tails(third_dx_head, third_dx_tail, third_dy_head,
                                  third_dy_tail, first_dx_head, first_dx_tail,
                                  first_dy_head, first_dy_tail))
        else:
            third_first_crossed_tails_tail = third_first_crossed_tails = (0,)
        if second_dx_tail:
            result_expansion = reduce(
                    sum_expansions,
                    _to_dx_extras(second_dx_tail_third_first_cross_product,
                                  second_dx_head, second_dx_tail,
                                  third_dy_tail, third_squared_length,
                                  first_dy_tail, first_squared_length,
                                  third_first_crossed_tails,
                                  third_first_crossed_tails_tail),
                    result_expansion)
        if second_dy_tail:
            result_expansion = reduce(
                    sum_expansions,
                    _to_dy_extras(second_dy_tail_third_first_cross_product,
                                  second_dy_head, second_dy_tail,
                                  third_first_crossed_tails,
                                  third_first_crossed_tails_tail),
                    result_expansion)
    if third_dx_tail or third_dy_tail:
        if first_dx_tail or first_dy_tail or second_dx_tail or second_dy_tail:
            first_second_crossed_tails_tail, first_second_crossed_tails = (
                _to_crossed_tails(first_dx_head, first_dx_tail, first_dy_head,
                                  first_dy_tail, second_dx_head,
                                  second_dx_tail, second_dy_head,
                                  second_dy_tail))
        else:
            first_second_crossed_tails_tail = first_second_crossed_tails = (0,)
        if third_dx_tail:
            result_expansion = reduce(
                    sum_expansions,
                    _to_dx_extras(third_dx_tail_first_second_cross_product,
                                  third_dx_head, third_dx_tail, first_dy_tail,
                                  first_squared_length, second_dy_tail,
                                  second_squared_length,
                                  first_second_crossed_tails,
                                  first_second_crossed_tails_tail),
                    result_expansion)
        if third_dy_tail:
            result_expansion = reduce(
                    sum_expansions,
                    _to_dy_extras(third_dy_tail_first_second_cross_product,
                                  third_dy_head, third_dy_tail,
                                  first_second_crossed_tails,
                                  first_second_crossed_tails_tail),
                    result_expansion)
    return result_expansion[-1]


def _to_dx_extras(head: Expansion,
                  dx_head: Real,
                  dx_tail: Real,
                  left_dy_tail: Real,
                  left_squared_length: Expansion,
                  right_dy_tail: Real,
                  right_squared_length: Expansion,
                  left_right_crossed_tails_head: Expansion,
                  left_right_crossed_tails_tail: Expansion
                  ) -> Iterable[Expansion]:
    dx_tail_left_right_crossed_tails = scale_expansion(
            left_right_crossed_tails_head, dx_tail)
    yield sum_expansions(scale_expansion(head, dx_tail),
                         scale_expansion(dx_tail_left_right_crossed_tails,
                                         2 * dx_head))
    if left_dy_tail:
        yield scale_expansion(scale_expansion(right_squared_length, dx_tail),
                              left_dy_tail)
    if right_dy_tail:
        yield scale_expansion(scale_expansion(left_squared_length, -dx_tail),
                              right_dy_tail)
    first_addend = scale_expansion(dx_tail_left_right_crossed_tails, dx_tail)
    dx_tail_left_right_crossed_tails_tail = scale_expansion(
            left_right_crossed_tails_tail, dx_tail)
    second_addend = sum_expansions(
            scale_expansion(dx_tail_left_right_crossed_tails_tail,
                            2 * dx_head),
            scale_expansion(dx_tail_left_right_crossed_tails_tail, dx_tail))
    yield sum_expansions(first_addend, second_addend)


def _to_dy_extras(expansion: Expansion,
                  dy_head: Real,
                  dy_tail: Real,
                  rest_crossed_tails_head: Expansion,
                  rest_crossed_tails_tail: Expansion) -> Iterable[Expansion]:
    dy_tail_rest_crossed_tails = scale_expansion(rest_crossed_tails_head,
                                                 dy_tail)
    yield sum_expansions(scale_expansion(expansion, dy_tail),
                         scale_expansion(dy_tail_rest_crossed_tails,
                                         2 * dy_head))
    first_addend = scale_expansion(dy_tail_rest_crossed_tails, dy_tail)
    dy_tail_rest_crossed_tails_tail = scale_expansion(rest_crossed_tails_tail,
                                                      dy_tail)
    second_addend = sum_expansions(
            scale_expansion(dy_tail_rest_crossed_tails_tail, 2 * dy_head),
            scale_expansion(dy_tail_rest_crossed_tails_tail, dy_tail))
    yield sum_expansions(first_addend, second_addend)


def _to_extra(head: Expansion,
              coordinate: Real,
              coordinate_tail: Real,
              left_coordinate: Real,
              left_squared_length: Expansion,
              right_coordinate: Real,
              right_squared_length: Expansion) -> Expansion:
    second_addend = scale_expansion(scale_expansion(right_squared_length,
                                                    coordinate_tail),
                                    left_coordinate)
    first_addend = scale_expansion(head, 2 * coordinate)
    minuend = sum_expansions(first_addend, second_addend)
    subtrahend = scale_expansion(scale_expansion(left_squared_length,
                                                 coordinate_tail),
                                 -right_coordinate)
    return sum_expansions(subtrahend, minuend)


def _to_crossed_tails(left_dx_head: Real,
                      left_dx_tail: Real,
                      left_dy_head: Real,
                      left_dy_tail: Real,
                      right_dx_head: Real,
                      right_dx_tail: Real,
                      right_dy_head: Real,
                      right_dy_tail: Real) -> Tuple[Expansion, Expansion]:
    tail = two_two_diff(*two_product(left_dx_tail, right_dy_tail),
                        *two_product(right_dx_tail, left_dy_tail))
    head = sum_expansions(two_two_sum(*two_product(left_dx_tail,
                                                   right_dy_head),
                                      *two_product(left_dx_head,
                                                   right_dy_tail)),
                          two_two_sum(*two_product(right_dx_tail,
                                                   -left_dy_head),
                                      *two_product(right_dx_head,
                                                   -left_dy_tail)))
    return tail, head


def _multiply_by_squared_length(head: Expansion,
                                dx_head: Real,
                                dy_head: Real) -> Expansion:
    return sum_expansions(scale_expansion(scale_expansion(head, dx_head),
                                          dx_head),
                          scale_expansion(scale_expansion(head, dy_head),
                                          dy_head))


def _to_addend(left_dx_head: Real,
               left_dx_tail: Real,
               left_dy_head: Real,
               left_dy_tail: Real,
               mid_dx_head: Real,
               mid_dx_tail: Real,
               mid_dy_head: Real,
               mid_dy_tail: Real,
               right_dx_head: Real,
               right_dx_tail: Real,
               right_dy_head: Real,
               right_dy_tail: Real) -> Real:
    return ((left_dx_head * left_dx_head + left_dy_head * left_dy_head)
            * ((mid_dx_head * right_dy_tail + right_dy_head * mid_dx_tail)
               - (mid_dy_head * right_dx_tail + right_dx_head * mid_dy_tail))
            + 2 * (left_dx_head * left_dx_tail + left_dy_head * left_dy_tail)
            * (mid_dx_head * right_dy_head - mid_dy_head * right_dx_head))


def _to_squared_length(dx_head: Real, dy_head: Real) -> Expansion:
    dx_squared_tail, dx_squared = square(dx_head)
    dy_squared_tail, dy_squared = square(dy_head)
    return two_two_sum(dx_squared_tail, dx_squared, dy_squared_tail,
                       dy_squared)
