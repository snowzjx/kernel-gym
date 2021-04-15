from typing import Union

import numpy as np

from kernel_gym.service.proto import ScalarRange

observation_t = Union[np.ndarray, int]


def scalar_range2tuple(sr: ScalarRange, defaults=(-np.inf, np.inf)):
    """Convert a ScalarRange to a tuple of (min, max) bounds."""
    return (
        sr.min.value if sr.HasField("min") else defaults[0],
        sr.max.value if sr.HasField("max") else defaults[1],
    )
