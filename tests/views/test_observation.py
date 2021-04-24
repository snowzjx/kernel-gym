from unittest import TestCase
import pytest
from kernel_gym.service.proto import (
    StepRequest,
    StepReply,
    PbObservation,
    PbObservationSpace,
    PbScalarRange,
    PbScalarRangeList,
    PbScalarLimit,
    PbInt64List,
)
from kernel_gym.views import (
    ObservationView,
    ObservationSpace,
)
from kernel_gym.dsl import Observer


class MockGetObservationReply(object):
    def __init__(self, value):
        self.observation = [value]


class MockGetObservation(object):

    def __init__(self, ret=None):
        self.called_observation_spaces = []
        self.ret = list(reversed(ret or []))

    def __call__(self, request: StepRequest):
        self.called_observation_spaces.append(request.observation_space_index[0])
        ret = self.ret[-1]
        del self.ret[-1]
        return MockGetObservationReply(ret)


spaces = [
    (
        Observer("mock function"),
        PbObservationSpace(
            name="cc",
            int64_range_list=PbScalarRangeList(
                range=[
                    PbScalarRange(
                        min=PbScalarLimit(value=-100), max=PbScalarLimit(value=100)
                    ),
                    PbScalarRange(
                        min=PbScalarLimit(value=-100), max=PbScalarLimit(value=100)
                    ),
                ]
            ),
        )
    )
]


class TestObservation(TestCase):

    def test_empty_space(self):
        with pytest.raises(ValueError) as ctx:
            ObservationView(MockGetObservation(), [])
        assert str(ctx.value) == "No observation spaces"
        print("test_empty_space passed ...")

    def test_invalid_observation_name(self):
        observation = ObservationView(MockGetObservation(), spaces)
        with pytest.raises(KeyError) as ctx:
            _ = observation["invalid"]
        assert str(ctx.value) == "'invalid'"
        print("test_invalid_observation_name passed ...")

    def test_get_observation_with_name(self):
        mock = MockGetObservation(
            ret=[
                PbObservation(int64_list=PbInt64List(value=[-5, 15]))
            ]
        )
        observation = ObservationView(mock, spaces)
        print(observation["cc"])
        print("test_get_observation_with_name passed ...")

    def test_get_observation_with_attr(self):
        mock = MockGetObservation(
            ret=[
                PbObservation(int64_list=PbInt64List(value=[-5, 15]))
            ]
        )
        observation = ObservationView(mock, spaces)
        print(observation.cc())
        print("test_get_observation_with_attr passed ...")
