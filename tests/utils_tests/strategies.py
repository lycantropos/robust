from functools import partial
from itertools import product
from typing import Sequence

from hypothesis import strategies

from robust.utils import (split,
                          square,
                          two_diff,
                          two_product,
                          two_sum)
from tests.strategies import (scalars_strategies,
                              scalars_strategies_factories)
from tests.utils import (Domain,
                         cleave,
                         combine,
                         compose,
                         extend_function,
                         identity,
                         pack,
                         to_builder,
                         to_pairs,
                         tuple_map)

scalars = scalars_strategies.flatmap(identity)
scalars_pairs = scalars_strategies.flatmap(to_pairs)
zeros_with_scalars = strategies.one_of(
        [strategies.tuples(strategies.builds(type_), factory())
         for type_, factory in scalars_strategies_factories.items()])
reverse_sorted_by_modulus_scalars_pairs = (scalars_pairs
                                           .map(partial(sorted,
                                                        key=abs,
                                                        reverse=True)))

scalars_pairs_strategies = scalars_strategies.map(to_pairs)
unary_expanding_functions = (split, square)
binary_expanding_functions = (two_diff, two_product, two_sum)
non_overlapping_scalars_pairs = strategies.one_of(
        [scalars_strategies.flatmap(to_builder(function))
         for function in unary_expanding_functions]
        + [scalars_pairs_strategies.flatmap(to_builder(pack(function)))
           for function in binary_expanding_functions])
non_overlapping_scalars_pairs_pairs = strategies.one_of(
        scalars_pairs_strategies.flatmap(to_builder(extend_function(split))),
        scalars_pairs_strategies.flatmap(to_builder(extend_function(square))),
        *[(scalars_pairs_strategies
           .map(to_pairs)
           .flatmap(to_builder(extend_function(pack(function)))))
          for function in binary_expanding_functions])


def expand(value: Domain) -> Sequence[Domain]:
    return value,


unary_expanding_functions = (expand,) + unary_expanding_functions
expansions_builders = (tuple_map(to_builder, unary_expanding_functions)
                       + tuple(compose(to_builder(pack(function)), to_pairs)
                               for function in binary_expanding_functions))
zero_expansions_with_scalars = (zeros_with_scalars
                                .map(combine(expand, identity)))
expansions_with_zeros = strategies.one_of(
        [strategies.tuples(builder(factory()), strategies.builds(type_))
         for type_, factory in scalars_strategies_factories.items()
         for builder in expansions_builders])
expansions_with_scales = strategies.one_of(
        [scalars_strategies.flatmap(compose(pack(strategies.tuples),
                                            cleave(builder, identity)))
         for builder in expansions_builders])
expansions_pairs = strategies.one_of(
        [scalars_strategies.flatmap(compose(pack(strategies.tuples),
                                            cleave(builder, other_builder)))
         for builder, other_builder in product(expansions_builders,
                                               repeat=2)])
