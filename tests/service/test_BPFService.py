from unittest import TestCase

from bcc import BPF

from kernel_gym.service import BPFService
from kernel_gym.dsl import Function


class TestBPFService(TestCase):

    def test_create_service(self):
        service = BPFService("test")
        func1 = Function("tcp_connect") \
            .header("net/sock.h") \
            .arg("struct sock*", "sk").extract("__sk_common.skc_rcv_saddr").extract("__sk_common.skc_daddr") \
            .next()
        func2 = Function("tcp_v4_connect") \
            .header("net/sock.h") \
            .arg("struct sock*", "sk").extract("__sk_common.skc_rcv_saddr").extract("__sk_common.skc_daddr") \
            .next()

        service.add_bpf_function(func1)
        service.add_bpf_function(func2)
        bpf_prog = service.render()
        print(bpf_prog)
        BPF(text=bpf_prog)