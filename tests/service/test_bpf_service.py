from unittest import TestCase

from kernel_gym.dsl import Observer
from kernel_gym.service import BPFConnection
from kernel_gym.service.bpf import BPFRender
from kernel_gym.service.proto import InstallObserverRequest, StepRequest


class TestBPFService(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBPFService, self).__init__(*args, **kwargs)
        self._connection = BPFConnection('localhost:50051')

    def test_install_observer(self):
        observer_name = "srtt"
        render = BPFRender(observer_name)
        observer = Observer("tcp_rcv_established") \
            .header("net/sock.h") \
            .arg("struct sock*", "sk").extract("__sk_common.skc_rcv_saddr").extract("__sk_common.skc_daddr") \
            .next()

        render.add_bpf_function(observer)
        bpf_prog = render.render()
        print(bpf_prog)

        request = InstallObserverRequest(name=observer_name, bpf_program=bpf_prog)
        self._connection(self._connection.stub.InstallObserver, request)

    def test_step(self):
        request = StepRequest()
        self._connection(self._connection.stub.Step, request)
