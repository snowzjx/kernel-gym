from bcc import BPF

prog: str = '''
#include <uapi/linux/ptrace.h>
#include <net/sock.h>

int kprobe__tcp_connect(struct pt_regs *ctx, struct sock *sk) { 
    bpf_trace_printk("sk: %d\\n", &sk->__sk_common.skc_rcv_saddr);
    return 0; 
}
'''


def main():
    bpf = BPF(text=prog)
    # bpf.attach_kprobe(event=bpf.get_syscall_fnname("clone"), fn_name="kprobe__sys_clone")
    bpf.trace_print()


if __name__ == "__main__":
    main()
