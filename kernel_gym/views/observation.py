from typing import List, Dict, Tuple, Callable
from kernel_gym.service.proto import PbObservationSpace
from kernel_gym.service.proto import StepRequest, StepReply
from kernel_gym.dsl import Function
from .observation_space import ObservationSpace


class ObservationView(object):
    def __init__(
            self,
            get_observation: Callable[[StepRequest], StepReply],
            spaces: List[Tuple[Function, PbObservationSpace]]):
        if not spaces:
            raise ValueError("No observation spaces")
        self.spaces: Dict[str, ObservationSpace] = {}
        self._get_observation = get_observation
        self.session_id = -1
        for i, s in enumerate(spaces):
            self._add_space(ObservationSpace.from_proto(i, s[0], s[1]))

    def __getitem__(self, observation_space_id: str):
        space = self.spaces[observation_space_id]
        request = StepRequest(
            session_id=self.session_id,
            observation_space_index=[space.index],
        )
        reply: StepReply = self._get_observation(request)
        if len(reply.observation) != 1:
            raise ValueError(
                f"Requested 1 observation but received {len(reply.observation)}"
            )
        return space.translate(reply.observation[0])

    def _add_space(self, space: ObservationSpace):
        self.spaces[space.id] = space
        setattr(self, space.id, lambda: self[space.id])

    def __repr__(self):
        return f"ObservationView[{', '.join(sorted(self.spaces.keys()))}]"
