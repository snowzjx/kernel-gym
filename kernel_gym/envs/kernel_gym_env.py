import gym
from typing import Optional
from kernel_gym.views import ObservationView


class KernelGym(gym.Env):
    """ An OpenAI gym environment for kernel function optimization.

    """

    def __init__(self,
                 observation_space: Optional[ObservationView]):
        pass

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass
