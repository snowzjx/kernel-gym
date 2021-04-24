from unittest import TestCase

from kernel_gym.dsl import Function
from kernel_gym.service import BPFConnection
from kernel_gym.service.bpf import BPFRender
from kernel_gym.service.proto import StartBPFRequest, StepRequest


class TestBPFService(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBPFService, self).__init__(*args, **kwargs)
        self._connection = BPFConnection('localhost:50051')

    def test_create_bpf_prog(self):
        render = BPFRender("test")
        func = Function("tcp_connect") \
            .header("net/sock.h") \
            .arg("struct sock*", "sk").extract("__sk_common.skc_rcv_saddr").extract("__sk_common.skc_daddr") \
            .next()

        render.add_bpf_function(func)
        bpf_prog = render.render()
        print(bpf_prog)

        request = StartBPFRequest(bpf_program=bpf_prog)
        self._connection(self._connection.stub.StartBPF, request)

    def test_step(self):
        request = StepRequest()
        self._connection(self._connection.stub.Step, request)
