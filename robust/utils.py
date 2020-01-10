from typing import Tuple

from . import bounds
from .hints import (Expansion,
                    Point,
                    Scalar)

X, Y = 0, 1


def fast_two_sum(left: Scalar, right: Scalar) -> Tuple[Scalar, Scalar]:
    estimation = left + right
    right_virtual = estimation - left
    tail = right - right_virtual
    return estimation, tail


def two_sum(left: Scalar, right: Scalar) -> Tuple[Scalar, Scalar]:
    estimation = left + right
    right_virtual = estimation - left
    left_virtual = estimation - right_virtual
    right_tail = right - right_virtual
    left_tail = left - left_virtual
    tail = left_tail + right_tail
    return estimation, tail


def split(value: Scalar,
          *,
          splitter: Scalar = bounds.splitter) -> Tuple[Scalar, Scalar]:
    base = splitter * value
    high = base - (base - value)
    low = value - high
    return low, high


def two_product_presplit(left: Scalar, right: Scalar, right_low: Scalar,
                         right_high: Scalar) -> Tuple[Scalar, Scalar]:
    estimation = left * right
    left_low, left_high = split(left)
    first_error = estimation - left_high * right_high
    second_error = first_error - left_low * right_high
    third_error = second_error - left_high * right_low
    tail = left_low * right_low - third_error
    return estimation, tail


def two_product(left: Scalar, right: Scalar) -> Tuple[Scalar, Scalar]:
    estimation = left * right
    left_low, left_high = split(left)
    right_low, right_high = split(right)
    first_error = estimation - left_high * right_high
    second_error = first_error - left_low * right_high
    third_error = second_error - left_high * right_low
    tail = left_low * right_low - third_error
    return estimation, tail


def two_two_diff(left_tail: Scalar, left: Scalar, right_tail: Scalar,
                 right: Scalar) -> Tuple[Scalar, Scalar, Scalar, Scalar]:
    interim, interim_tail, third_tail = two_one_diff(left_tail, left,
                                                     right_tail)
    estimation, first_tail, second_tail = two_one_diff(interim_tail, interim,
                                                       right)
    return third_tail, second_tail, first_tail, estimation


def two_two_sum(left_tail: Scalar, left: Scalar, right_tail: Scalar,
                right: Scalar) -> Tuple[Scalar, Scalar, Scalar, Scalar]:
    interim, interim_tail, third_tail = two_one_sum(left_tail, left,
                                                    right_tail)
    estimation, first_tail, second_tail = two_one_sum(interim_tail, interim,
                                                      right)
    return third_tail, second_tail, first_tail, estimation


def two_one_sum(left_tail: Scalar, left: Scalar,
                right: Scalar) -> Tuple[Scalar, Scalar, Scalar]:
    interim, second_tail = two_sum(left_tail, right)
    estimation, first_tail = two_sum(left, interim)
    return estimation, first_tail, second_tail


def two_one_diff(left_tail: Scalar, left: Scalar,
                 right: Scalar) -> Tuple[Scalar, Scalar, Scalar]:
    interim, second_tail = two_diff(left_tail, right)
    estimation, first_tail = two_sum(left, interim)
    return estimation, first_tail, second_tail


def two_diff(left: Scalar, right: Scalar) -> Tuple[Scalar, Scalar]:
    estimation = left - right
    return estimation, two_diff_tail(left, right, estimation)


def two_diff_tail(left: Scalar, right: Scalar, estimation: Scalar) -> Scalar:
    right_virtual = left - estimation
    left_virtual = estimation + right_virtual
    right_error = right_virtual - right
    left_error = left - left_virtual
    return left_error + right_error


def square(value: Scalar) -> Tuple[Scalar, Scalar]:
    estimation = value * value
    value_low, value_high = split(value)
    first_error = estimation - value_high * value_high
    second_error = first_error - (value_high + value_high) * value_low
    tail = value_low * value_low - second_error
    return estimation, tail


def sum_expansions(left_expansion: Expansion,
                   right_expansion: Expansion) -> Expansion:
    """
    Sums two expansions with zero components elimination.
    """
    left_length = len(left_expansion)
    right_length = len(right_expansion)
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
            accumulator, tail = fast_two_sum(left_element, accumulator)
            left_index += 1
            try:
                left_element = left_expansion[left_index]
            except IndexError:
                pass
        else:
            accumulator, tail = fast_two_sum(right_element, accumulator)
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
                accumulator, tail = two_sum(accumulator, left_element)
                left_index += 1
                try:
                    left_element = left_expansion[left_index]
                except IndexError:
                    pass
            else:
                accumulator, tail = two_sum(accumulator, right_element)
                right_index += 1
                try:
                    right_element = right_expansion[right_index]
                except IndexError:
                    pass
            if tail:
                result.append(tail)
    while left_index < left_length:
        accumulator, tail = two_sum(accumulator, left_element)
        left_index += 1
        try:
            left_element = left_expansion[left_index]
        except IndexError:
            pass
        if tail:
            result.append(tail)
    while right_index < right_length:
        accumulator, tail = two_sum(accumulator, right_element)
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


def scale_expansion(expansion: Expansion, scalar: Scalar) -> Expansion:
    """
    Multiplies an expansion by a scalar with zero components elimination.
    """
    expansion = iter(expansion)
    scalar_low, scalar_high = split(scalar)
    accumulator, tail = two_product_presplit(next(expansion), scalar,
                                             scalar_low, scalar_high)
    result = []
    if tail:
        result.append(tail)
    for element in expansion:
        product, product_tail = two_product_presplit(element, scalar,
                                                     scalar_low, scalar_high)
        interim, tail = two_sum(accumulator, product_tail)
        if tail:
            result.append(tail)
        accumulator, tail = fast_two_sum(product, interim)
        if tail:
            result.append(tail)
    if accumulator or not result:
        result.append(accumulator)
    return result


def to_cross_product(minuend_multiplier_x: Scalar,
                     minuend_multiplier_y: Scalar,
                     subtrahend_multiplier_x: Scalar,
                     subtrahend_multiplier_y: Scalar) -> Expansion:
    """
    Returns expansion of vectors' planar cross product.
    """
    minuend, minuend_tail = two_product(minuend_multiplier_x,
                                        minuend_multiplier_y)
    subtrahend, subtrahend_tail = two_product(subtrahend_multiplier_y,
                                              subtrahend_multiplier_x)
    return two_two_diff(minuend_tail, minuend, subtrahend_tail, subtrahend)


def to_perpendicular_point(point: Point) -> Point:
    return -point[Y], point[X]
