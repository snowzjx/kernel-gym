from __future__ import annotations
from kernel_gym.dsl import Function


def main():
    obs1 = Function("fun1") \
        .arg("arg1_type", "arg1_type").extract("prop1") \
        .next() \
        .arg("arg2_type", "arg2_type").extract("prop2").rescale(0, 100) \
        .next()

    print(obs1.to_bpf_prog())


if __name__ == "__main__":
    main()
