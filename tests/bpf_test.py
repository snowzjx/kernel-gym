from bcc import BPF

prog: str = '''
int kprobe__sys_clone(void *ctx) { 
    bpf_trace_printk("Hello, World!\\n"); 
    return 0; 
}
'''


def main():
    bpf = BPF(text=prog)
    bpf.attach_kprobe(event=bpf.get_syscall_fnname("clone"), fn_name="kprobe__sys_clone")
    bpf.trace_print()


if __name__ == "__main__":
    main()
