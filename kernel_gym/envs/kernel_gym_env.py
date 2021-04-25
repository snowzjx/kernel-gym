import logging
from typing import Optional
from kernel_gym.service.bpf_connection import BPFConnection

import gym
from kernel_gym.views import (
    ObservationView,
    ObservationSpace
)


class KernelGym(gym.Env):
    """ An OpenAI gym environment for kernel function optimization.

    """

    def __init__(
            self,
            service_endpoint: str,
            observation_space: Optional[ObservationView],
            logging_level: Optional[int] = None
    ):
        self.logger = logging.getLogger("compiler_gym.envs")
        if logging_level is None:
            logging_level = logging.DEBUG
        self.logger.setLevel(logging_level)

        self._session_id: Optional[int] = None

        self.service = BPFConnection(
            endpoint=service_endpoint,
            logger=self.logger)

        # TODO Setup backend BPF service

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass
