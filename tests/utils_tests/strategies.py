from functools import partial
from itertools import product
from typing import Sequence

from hypothesis import strategies

from robust.utils import (split,
                          square,
                          two_diff,
                          two_product,
                          two_sum)
from tests.strategies import (numbers_strategies,
                              numbers_strategies_factories)
from tests.utils import (Domain,
                         cleave_in_tuples,
                         combine,
                         compose,
                         extend_function,
                         identity,
                         pack,
                         to_builder,
                         to_pairs,
                         to_quadruples,
                         tuple_map)

numbers = numbers_strategies.flatmap(identity)
numbers_pairs = numbers_strategies.flatmap(to_pairs)
numbers_quadruples = numbers_strategies.flatmap(to_quadruples)
zeros_with_numbers = strategies.one_of(
        [strategies.tuples(strategies.builds(type_), factory())
         for type_, factory in numbers_strategies_factories.items()])
reverse_sorted_by_modulus_numbers_pairs = (numbers_pairs
                                           .map(partial(sorted,
                                                        key=abs,
                                                        reverse=True)))

numbers_pairs_strategies = numbers_strategies.map(to_pairs)
unary_expanding_functions = (split, square)
binary_expanding_functions = (two_diff, two_product, two_sum)
non_overlapping_real_numbers_pairs = strategies.one_of(
        [numbers_strategies.flatmap(to_builder(function))
         for function in unary_expanding_functions]
        + [numbers_pairs_strategies.flatmap(to_builder(pack(function)))
           for function in binary_expanding_functions])
non_overlapping_real_numbers_pairs_pairs = strategies.one_of(
        numbers_pairs_strategies.flatmap(to_builder(extend_function(split))),
        numbers_pairs_strategies.flatmap(to_builder(extend_function(square))),
        *[(numbers_pairs_strategies
           .map(to_pairs)
           .flatmap(to_builder(extend_function(pack(function)))))
          for function in binary_expanding_functions])


def expand(value: Domain) -> Sequence[Domain]:
    return value,


unary_expanding_functions = (expand,) + unary_expanding_functions
expansions_builders = (tuple_map(to_builder, unary_expanding_functions)
                       + tuple(compose(to_builder(pack(function)), to_pairs)
                               for function in binary_expanding_functions))
zero_expansions_with_numbers = (zeros_with_numbers
                                .map(combine(expand, identity)))
expansions_with_zeros = strategies.one_of(
        [strategies.tuples(builder(factory()), strategies.builds(type_))
         for type_, factory in numbers_strategies_factories.items()
         for builder in expansions_builders])
expansions_with_scales = strategies.one_of(
        [numbers_strategies.flatmap(cleave_in_tuples(builder, identity))
         for builder in expansions_builders])
expansions_pairs = strategies.one_of(
        [numbers_strategies.flatmap(cleave_in_tuples(builder, other_builder))
         for builder, other_builder in product(expansions_builders,
                                               repeat=2)])
