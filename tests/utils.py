from itertools import combinations
from typing import (Callable,
                    Tuple,
                    TypeVar)

from hypothesis.strategies import SearchStrategy

from robust.hints import (Expansion,
                          Scalar)

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy


def implication(antecedent: bool, consequent: bool) -> bool:
    return not antecedent or consequent


def identity(value: Domain) -> Domain:
    return value


def is_sorted_by_magnitude_expansion(expansion: Expansion,
                                     *,
                                     zero_eliminated: bool = False) -> bool:
    return all(abs(element) <= abs(next_element)
               or not zero_eliminated and next_element == 0
               for element, next_element in zip(expansion, expansion[1:]))


def is_non_overlapping_expansion(expansion: Expansion) -> bool:
    return all(are_non_overlapping_numbers(element, other_element)
               for element, other_element in combinations(expansion, 2))


def are_non_overlapping_numbers(left: Scalar, right: Scalar) -> bool:
    left_binary, right_binary = (scalar_to_binary(abs(left)),
                                 scalar_to_binary(abs(right)))
    left_whole_part, left_fractional_part = split_binary(left_binary)
    right_whole_part, right_fractional_part = split_binary(right_binary)
    return (are_non_overlapping_whole_parts(left_whole_part, right_whole_part)
            and are_non_overlapping_fractional_parts(left_fractional_part,
                                                     right_fractional_part))


def split_binary(binary: str) -> Tuple[str, str]:
    left_whole_part, _, left_fractional_part = binary.partition('.')
    return left_whole_part, left_fractional_part


def are_non_overlapping_whole_parts(left: str, right: str) -> bool:
    max_length = max(len(left), len(right))
    return all(not (left_character == '1' and right_character == '1')
               for (left_character,
                    right_character) in zip(left.rjust(max_length, '0'),
                                            right.rjust(max_length, '0')))


def are_non_overlapping_fractional_parts(left: str, right: str) -> bool:
    max_length = max(len(left), len(right))
    return all(not (left_character == '1' and right_character == '1')
               for (left_character,
                    right_character) in zip(left.ljust(max_length, '0'),
                                            right.ljust(max_length, '0')))


def scalar_to_binary(number: Scalar) -> str:
    if isinstance(number, int):
        return '{:b}'.format(number)
    else:
        return float_to_binary(number
                               if isinstance(number, float)
                               else float(number))


def float_to_binary(number: float,
                    *,
                    hex_digit_to_bin: Callable[[str], str] =
                    {'{:x}'.format(digit): '{:04b}'.format(digit)
                     for digit in range(16)}.__getitem__) -> str:
    if number < 0:
        return '-' + float_to_binary(-number)
    elif number == 0:
        return '0.'
    mantissa, exponent = number.hex()[2:].split('p')
    exponent = int(exponent)
    mantissa = mantissa.rstrip('0')
    digits = mantissa[0] + mantissa[2:]
    if exponent < 0:
        prefix, suffix = '0' * -exponent, ''
        exponent = 0
    else:
        prefix, suffix = '', '0' * exponent
    result = (prefix
              + (''.join(map(hex_digit_to_bin,
                             digits[:1 + exponent])).lstrip('0') or '0')
              + ''.join(map(hex_digit_to_bin, digits[1 + exponent:]))
              + suffix)
    return result[:1 + exponent] + '.' + result[1 + exponent:].rstrip('0')
