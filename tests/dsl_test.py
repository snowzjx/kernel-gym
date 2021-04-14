from __future__ import annotations
from kernel_gym.dsl import Function
from bcc import BPF


def main():
    f1 = Function("tcp_connect") \
        .header("net/sock.h") \
        .arg("struct sock*", "sk").extract("__sk_common.skc_rcv_saddr").extract("__sk_common.skc_daddr") \
        .next()
    bpf_code = f1.to_bpf_prog()
    print(bpf_code)
    b = BPF(text=bpf_code)


if __name__ == "__main__":
    main()