from tests.strategies import numbers_strategies
from tests.utils import (to_pairs,
                         to_triplets)

points_strategies = numbers_strategies.map(to_pairs)
points_pairs = points_strategies.flatmap(to_pairs)
points_triplets = points_strategies.flatmap(to_triplets)
