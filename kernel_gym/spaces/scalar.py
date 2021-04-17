import random
from gym.spaces import Space
from typing import Optional


class Scalar(Space):
    """A scalar value."""

    __slots__ = ["min", "max", "dtype"]

    def __init__(
        self, min: Optional[float] = None, max: Optional[float] = None, dtype=float
    ):
        self.min = min
        self.max = max
        self.dtype = dtype

    def sample(self):
        min = 0 if self.min is None else self.min
        max = 1 if self.max is None else self.max
        return self.dtype(random.uniform(min, max))

    def contains(self, x):
        if not isinstance(x, self.dtype):
            return False
        min = -float("inf") if self.min is None else self.min
        max = float("inf") if self.max is None else self.max
        return min <= x <= max

    def __repr__(self):
        if self.min is None and self.max is None:
            return self.dtype.__name__
        lower_bound = "-inf" if self.min is None else self.min
        upper_bound = "inf" if self.max is None else self.max
        return f"{self.dtype.__name__}<{lower_bound},{upper_bound}>"

    def __eq__(self, rhs):
        """Equality test."""
        if not isinstance(rhs, Scalar):
            return False
        return self.min == rhs.min and self.max == rhs.max and self.dtype == rhs.dtype