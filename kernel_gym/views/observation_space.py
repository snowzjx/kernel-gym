from __future__ import annotations

import numpy as np
from typing import Callable, Optional, Union

from gym.spaces import Space, Box
from kernel_gym.spaces import Scalar
from kernel_gym.service import observation_t, scalar_range2tuple
from kernel_gym.service.proto import PbObservationSpace, PbObservation
from kernel_gym.dsl import Function


class ObservationSpace(object):
    def __init__(
            self, id: str,
            index: int,
            dsl: Function,
            space: Space,
            translate: Callable[[Union[observation_t, PbObservation]], observation_t],
            to_string: Callable[[observation_t], str],
            default_value: observation_t):
        self.id = id
        self.index = index
        self.dsl = dsl
        self.space = space
        self.translate = translate
        self.to_string = to_string
        self.default_value = default_value

    def __repr__(self) -> str:
        return f"ObservationSpace({self.id})"

    def __eq__(self, rhs) -> bool:
        if not isinstance(rhs, ObservationSpace):
            return False
        return (
                self.id == rhs.id
                and self.index == rhs.index
                and self.space == rhs.space
                and self.default_value == rhs.default_value
        )

    @classmethod
    def from_proto(cls, index: int, dsl: Function, proto: PbObservationSpace):
        def make_box(scalar_range_list, dtype, defaults):
            bounds = [scalar_range2tuple(r, defaults) for r in scalar_range_list]
            return Box(
                low=np.array([b[0] for b in bounds], dtype=dtype),
                high=np.array([b[1] for b in bounds], dtype=dtype),
                dtype=dtype,
            )

        def make_scalar(scalar_range, dtype, defaults):
            scalar_range_tuple = scalar_range2tuple(scalar_range, defaults)
            return Scalar(
                min=scalar_range_tuple[0], max=scalar_range_tuple[1], dtype=dtype
            )

        shape_type = proto.WhichOneof("shape")

        if shape_type == "int64_range_list":
            space = make_box(
                proto.int64_range_list.range,
                np.int64,
                (np.iinfo(np.int64).min, np.iinfo(np.int64).max),
            )

            def translate(observation: PbObservation) -> observation_t:
                return np.array(observation.int64_list.value, dtype=np.int64)

            to_string = str

        elif shape_type == "scalar_int64_range":
            space = make_scalar(
                proto.scalar_int64_range,
                np.int64,
                (np.iinfo(np.int64).min, np.iinfo(np.int64).max),
            )

            def translate(observation: PbObservation) -> observation_t:
                return int(observation.scalar_int64)

            to_string = str

        else:
            raise TypeError(
                f"Unknown shape '{shape_type}' for ObservationSpace:\n{proto}"
            )

        return cls(
            id=proto.name,
            index=index,
            space=space,
            dsl=dsl,
            translate=translate,
            to_string=to_string,
            default_value=translate(proto.default_value),
        )

    def make_derived_space(
            self,
            id: str,
            dsl: Function,
            translate: Callable[[observation_t], observation_t],
            space: Optional[Space] = None,
            default_value: Optional[observation_t] = None,
            to_string: Callable[[observation_t], str] = None,
    ) -> ObservationSpace:
        return ObservationSpace(
            id=id,
            index=self.index,
            dsl=dsl,
            space=space or self.space,
            translate=lambda observation: translate(self.translate(observation)),
            to_string=to_string or self.to_string,
            default_value=(
                translate(self.default_value)
                if default_value is None
                else default_value
            ),
        )
