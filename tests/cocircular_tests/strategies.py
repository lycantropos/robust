from tests.strategies import numbers_strategies
from tests.utils import (to_pairs,
                         to_quadruples,
                         to_triplets)

points_strategies = numbers_strategies.map(to_pairs)
points_triplets = points_strategies.flatmap(to_triplets)
points_quadruples = points_strategies.flatmap(to_quadruples)
