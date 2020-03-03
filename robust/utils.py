from numbers import Real
from typing import Tuple

from . import bounds
from .hints import (Expansion,
                    Point)

X, Y = 0, 1


def fast_two_sum(left: Real, right: Real) -> Tuple[Real, Real]:
    estimation = left + right
    right_virtual = estimation - left
    tail = right - right_virtual
    return tail, estimation


def two_sum(left: Real, right: Real) -> Tuple[Real, Real]:
    estimation = left + right
    right_virtual = estimation - left
    left_virtual = estimation - right_virtual
    right_tail = right - right_virtual
    left_tail = left - left_virtual
    tail = left_tail + right_tail
    return tail, estimation


def split(value: Real,
          *,
          splitter: Real = bounds.splitter) -> Tuple[Real, Real]:
    base = splitter * value
    high = base - (base - value)
    low = value - high
    return low, high


def two_product_presplit(left: Real, right: Real, right_low: Real,
                         right_high: Real) -> Tuple[Real, Real]:
    estimation = left * right
    left_low, left_high = split(left)
    first_error = estimation - left_high * right_high
    second_error = first_error - left_low * right_high
    third_error = second_error - left_high * right_low
    tail = left_low * right_low - third_error
    return tail, estimation


def two_product(left: Real, right: Real) -> Tuple[Real, Real]:
    estimation = left * right
    left_low, left_high = split(left)
    right_low, right_high = split(right)
    first_error = estimation - left_high * right_high
    second_error = first_error - left_low * right_high
    third_error = second_error - left_high * right_low
    tail = left_low * right_low - third_error
    return tail, estimation


def two_two_diff(left_tail: Real, left: Real, right_tail: Real,
                 right: Real) -> Tuple[Real, Real, Real, Real]:
    third_tail, interim_tail, interim = two_one_diff(left_tail, left,
                                                     right_tail)
    second_tail, first_tail, estimation = two_one_diff(interim_tail, interim,
                                                       right)
    return third_tail, second_tail, first_tail, estimation


def two_two_sum(left_tail: Real, left: Real, right_tail: Real,
                right: Real) -> Tuple[Real, Real, Real, Real]:
    third_tail, interim_tail, interim = two_one_sum(left_tail, left,
                                                    right_tail)
    second_tail, first_tail, estimation = two_one_sum(interim_tail, interim,
                                                      right)
    return third_tail, second_tail, first_tail, estimation


def two_one_sum(left_tail: Real, left: Real,
                right: Real) -> Tuple[Real, Real, Real]:
    second_tail, interim = two_sum(left_tail, right)
    first_tail, estimation = two_sum(left, interim)
    return second_tail, first_tail, estimation


def two_one_diff(left_tail: Real, left: Real,
                 right: Real) -> Tuple[Real, Real, Real]:
    second_tail, interim = two_diff(left_tail, right)
    first_tail, estimation = two_sum(left, interim)
    return second_tail, first_tail, estimation


def two_diff(left: Real, right: Real) -> Tuple[Real, Real]:
    estimation = left - right
    return two_diff_tail(left, right, estimation), estimation


def two_diff_tail(left: Real, right: Real, estimation: Real) -> Real:
    right_virtual = left - estimation
    left_virtual = estimation + right_virtual
    right_error = right_virtual - right
    left_error = left - left_virtual
    return left_error + right_error


def square(value: Real) -> Tuple[Real, Real]:
    estimation = value * value
    value_low, value_high = split(value)
    first_error = estimation - value_high * value_high
    second_error = first_error - (value_high + value_high) * value_low
    tail = value_low * value_low - second_error
    return tail, estimation


def sum_expansions(left_expansion: Expansion,
                   right_expansion: Expansion) -> Expansion:
    """
    Sums two expansions with zero components elimination.
    """
    left_length, right_length = len(left_expansion), len(right_expansion)
    left_element, right_element = left_expansion[0], right_expansion[0]
    left_index = right_index = 0
    if (right_element > left_element) is (right_element > -left_element):
        accumulator = left_element
        left_index += 1
        try:
            left_element = left_expansion[left_index]
        except IndexError:
            pass
    else:
        accumulator = right_element
        right_index += 1
        try:
            right_element = right_expansion[right_index]
        except IndexError:
            pass
    result = []
    if (left_index < left_length) and (right_index < right_length):
        if (right_element > left_element) is (right_element > -left_element):
            tail, accumulator = fast_two_sum(left_element, accumulator)
            left_index += 1
            try:
                left_element = left_expansion[left_index]
            except IndexError:
                pass
        else:
            tail, accumulator = fast_two_sum(right_element, accumulator)
            right_index += 1
            try:
                right_element = right_expansion[right_index]
            except IndexError:
                pass
        if tail:
            result.append(tail)
        while (left_index < left_length) and (right_index < right_length):
            if ((right_element > left_element)
                    is (right_element > -left_element)):
                tail, accumulator = two_sum(accumulator, left_element)
                left_index += 1
                try:
                    left_element = left_expansion[left_index]
                except IndexError:
                    pass
            else:
                tail, accumulator = two_sum(accumulator, right_element)
                right_index += 1
                try:
                    right_element = right_expansion[right_index]
                except IndexError:
                    pass
            if tail:
                result.append(tail)
    while left_index < left_length:
        tail, accumulator = two_sum(accumulator, left_element)
        left_index += 1
        try:
            left_element = left_expansion[left_index]
        except IndexError:
            pass
        if tail:
            result.append(tail)
    while right_index < right_length:
        tail, accumulator = two_sum(accumulator, right_element)
        right_index += 1
        try:
            right_element = right_expansion[right_index]
        except IndexError:
            pass
        if tail:
            result.append(tail)
    if accumulator or not result:
        result.append(accumulator)
    return result


def scale_expansion(expansion: Expansion, scalar: Real) -> Expansion:
    """
    Multiplies an expansion by a scalar with zero components elimination.
    """
    expansion = iter(expansion)
    scalar_low, scalar_high = split(scalar)
    tail, accumulator = two_product_presplit(next(expansion), scalar,
                                             scalar_low, scalar_high)
    result = []
    if tail:
        result.append(tail)
    for element in expansion:
        product_tail, product = two_product_presplit(element, scalar,
                                                     scalar_low, scalar_high)
        tail, interim = two_sum(accumulator, product_tail)
        if tail:
            result.append(tail)
        tail, accumulator = fast_two_sum(product, interim)
        if tail:
            result.append(tail)
    if accumulator or not result:
        result.append(accumulator)
    return result


def to_cross_product(minuend_multiplier_x: Real,
                     minuend_multiplier_y: Real,
                     subtrahend_multiplier_x: Real,
                     subtrahend_multiplier_y: Real) -> Expansion:
    """
    Returns expansion of vectors' planar cross product.
    """
    minuend_tail, minuend = two_product(minuend_multiplier_x,
                                        minuend_multiplier_y)
    subtrahend_tail, subtrahend = two_product(subtrahend_multiplier_y,
                                              subtrahend_multiplier_x)
    return two_two_diff(minuend_tail, minuend, subtrahend_tail, subtrahend)


def to_perpendicular_point(point: Point) -> Point:
    return -point[Y], point[X]


def to_sign(value: Real) -> int:
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0
