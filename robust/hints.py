from decimal import Decimal
from numbers import Real
from typing import (Sequence,
                    Tuple,
                    TypeVar)

Scalar = TypeVar('Scalar', Real, Decimal)
Point = Tuple[Scalar, Scalar]
RealPoint = Tuple[Real, Real]
Expansion = Sequence[Real]
