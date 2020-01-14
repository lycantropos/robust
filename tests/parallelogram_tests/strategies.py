from tests.strategies import numbers_strategies
from tests.utils import (to_pairs,
                         to_quadruples)

points_strategies = numbers_strategies.map(to_pairs)
points_pairs = points_strategies.flatmap(to_pairs)
points_quadruples = points_strategies.flatmap(to_quadruples)
