import sys
from decimal import Decimal
from fractions import Fraction
from functools import partial
from typing import (Optional,
                    SupportsFloat)

from hypothesis import strategies

from robust.hints import Scalar
from tests.utils import Strategy

MAX_DIGITS_COUNT = sys.float_info.dig


def to_decimals(*,
                min_value: Optional[Scalar] = None,
                max_value: Optional[Scalar] = None,
                allow_nan: bool = False,
                allow_infinity: bool = False,
                max_digits_count: int = MAX_DIGITS_COUNT) -> Strategy[Decimal]:
    return (strategies.decimals(min_value=min_value,
                                max_value=max_value,
                                allow_nan=allow_nan,
                                allow_infinity=allow_infinity)
            .map(partial(to_digits_count,
                         max_digits_count=max_digits_count)))


def to_floats(*,
              min_value: Optional[Scalar] = None,
              max_value: Optional[Scalar] = None,
              allow_nan: bool = False,
              allow_infinity: bool = False,
              max_digits_count: int = MAX_DIGITS_COUNT) -> Strategy[float]:
    return (strategies.floats(min_value=min_value,
                              max_value=max_value,
                              allow_nan=allow_nan,
                              allow_infinity=allow_infinity)
            .map(partial(to_digits_count,
                         max_digits_count=max_digits_count)))


def to_fractions(*,
                 min_value: Optional[Scalar] = None,
                 max_value: Optional[Scalar] = None,
                 max_denominator: Optional[Scalar] = None,
                 max_digits_count: int = MAX_DIGITS_COUNT
                 ) -> Strategy[Fraction]:
    return (strategies.fractions(min_value=min_value,
                                 max_value=max_value,
                                 max_denominator=max_denominator)
            .map(partial(to_digits_count,
                         max_digits_count=max_digits_count)))


def to_integers(*,
                min_value: Optional[Scalar] = None,
                max_value: Optional[Scalar] = None,
                max_digits_count: int = MAX_DIGITS_COUNT) -> Strategy[int]:
    return (strategies.integers(min_value=min_value,
                                max_value=max_value)
            .map(partial(to_digits_count,
                         max_digits_count=max_digits_count)))


def to_digits_count(number: Scalar,
                    *,
                    max_digits_count: int = MAX_DIGITS_COUNT) -> Scalar:
    decimal = to_decimal(number).normalize()
    _, significant_digits, exponent = decimal.as_tuple()
    significant_digits_count = len(significant_digits)
    if exponent < 0:
        fixed_digits_count = (1 - exponent
                              if exponent <= -significant_digits_count
                              else significant_digits_count)
    else:
        fixed_digits_count = exponent + significant_digits_count
    if fixed_digits_count <= max_digits_count:
        return number
    whole_digits_count = max(significant_digits_count + exponent, 0)
    if whole_digits_count:
        whole_digits_offset = max(whole_digits_count - max_digits_count, 0)
        decimal /= 10 ** whole_digits_offset
        whole_digits_count -= whole_digits_offset
    else:
        decimal *= 10 ** (-exponent - significant_digits_count)
        whole_digits_count = 1
    decimal = round(decimal, max(max_digits_count - whole_digits_count, 0))
    return type(number)(str(decimal))


def to_decimal(number: SupportsFloat) -> Decimal:
    if isinstance(number, Decimal):
        return number
    elif not isinstance(number, (int, float)):
        number = float(number)
    return Decimal(number)


real_numbers_strategies_factories = {float: to_floats,
                                     Fraction: to_fractions,
                                     int: to_integers}
scalars_strategies_factories = {**real_numbers_strategies_factories,
                                Decimal: to_decimals}
real_numbers_strategies = strategies.sampled_from(
        [factory() for factory in real_numbers_strategies_factories.values()])
scalars_strategies = strategies.sampled_from(
        [factory() for factory in scalars_strategies_factories.values()])
