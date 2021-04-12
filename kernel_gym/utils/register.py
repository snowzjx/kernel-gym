from typing import List

import gym.envs

KERNEL_GYM_ENVS: List[str] = []


def register(id: str, **kwargs):
    KERNEL_GYM_ENVS.append(id)
    gym.envs.register(id=id, **kwargs)
