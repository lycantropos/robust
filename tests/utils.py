from functools import partial
from itertools import (combinations,
                       repeat)
from numbers import Real
from operator import itemgetter
from types import MappingProxyType
from typing import (Any,
                    Callable,
                    Dict,
                    Iterable,
                    Sequence,
                    Tuple,
                    TypeVar)

from hypothesis import strategies
from hypothesis.strategies import SearchStrategy

from robust.hints import Expansion

Domain = TypeVar('Domain')
Range = TypeVar('Range')
Strategy = SearchStrategy


def equivalence(left_statement: bool, right_statement: bool) -> bool:
    return left_statement is right_statement


def identity(value: Domain) -> Domain:
    return value


def extend_function(function: Callable[[Domain], Range]
                    ) -> Callable[[Tuple[Domain, ...]], Tuple[Range]]:
    return partial(tuple_map, function)


def tuple_map(function: Callable[[Domain], Range],
              values: Tuple[Domain, ...]) -> Tuple[Range, ...]:
    return tuple(map(function, values))


def pack(function: Callable[..., Range]
         ) -> Callable[[Iterable[Domain]], Range]:
    return partial(apply, function)


def apply(function: Callable[..., Range],
          args: Iterable[Domain],
          kwargs: Dict[str, Any] = MappingProxyType({})) -> Range:
    return function(*args, **kwargs)


def cleavage(functions: Tuple[Callable[[Domain], Range], ...],
             *args: Domain, **kwargs: Domain) -> Tuple[Range, ...]:
    return tuple(function(*args, **kwargs) for function in functions)


def cleave(*functions: Callable[[Domain], Range]
           ) -> Callable[[Tuple[Domain, ...]], Tuple[Range, ...]]:
    return partial(cleavage, functions)


def combination(functions: Tuple[Callable[[Domain], Range], ...],
                arguments: Tuple[Domain, ...]) -> Tuple[Range, ...]:
    return tuple(function(argument)
                 for function, argument in zip(functions, arguments))


def combine(*functions: Callable[[Domain], Range]
            ) -> Callable[[Tuple[Domain, ...]], Tuple[Range, ...]]:
    return partial(combination, functions)


def composition(functions: Tuple[Callable[[Domain], Range], ...],
                *args: Domain, **kwargs: Domain) -> Range:
    result = functions[-1](*args, **kwargs)
    for function in reversed(functions[:-1]):
        result = function(result)
    return result


def compose(*functions: Callable[..., Range]) -> Callable[..., Range]:
    return partial(composition, functions)


def cleave_in_tuples(*functions: Callable[[Strategy[Domain]], Strategy[Range]]
                     ) -> Callable[[Strategy[Domain]],
                                   Strategy[Tuple[Range, ...]]]:
    return compose(pack(strategies.tuples), cleave(*functions))


def to_tuples(elements: Strategy[Domain],
              *,
              size: int) -> Strategy[Tuple[Domain, ...]]:
    return strategies.tuples(*repeat(elements,
                                     times=size))


to_pairs = partial(to_tuples,
                   size=2)
to_triplets = partial(to_tuples,
                      size=3)
to_quadruples = partial(to_tuples,
                        size=4)


def to_builder(function: Callable[[Domain], Range]
               ) -> Callable[[Strategy[Domain]], Strategy[Range]]:
    return partial(strategies.builds, function)


def is_sorted_by_magnitude_expansion(expansion: Expansion,
                                     *,
                                     zero_eliminated: bool = False) -> bool:
    return all(abs(element) <= abs(next_element)
               or not zero_eliminated and next_element == 0
               for element, next_element in zip(expansion, expansion[1:]))


def is_non_overlapping_expansion(expansion: Expansion) -> bool:
    return all(are_non_overlapping_numbers(element, other_element)
               for element, other_element in combinations(expansion, 2))


def are_non_overlapping_numbers(left: Real, right: Real) -> bool:
    left_binary, right_binary = (number_to_binary(abs(left)),
                                 number_to_binary(abs(right)))
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


def number_to_binary(number: Real) -> str:
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


Permutation = Sequence[int]


def is_even_permutation(permutation: Permutation) -> bool:
    if len(permutation) == 1:
        return True
    transitions_count = 0
    for index, element in enumerate(permutation):
        for next_element in permutation[index + 1:]:
            if element > next_element:
                transitions_count += 1
    return not (transitions_count % 2)


def permute(sequence: Sequence[Domain],
            permutation: Permutation) -> Sequence[Domain]:
    return itemgetter(*permutation)(sequence)
