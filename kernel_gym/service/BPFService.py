from typing import List, Set
from bcc import BPF
from kernel_gym.dsl import Function
from kernel_gym.service.bpf import BPFTemplate
from jinja2 import Template
from jinja2 import Environment


class BPFService:
    def __init__(self, map_name: str):
        # bpf_map_create_command = f"BPF_HASH({map_name}, int, int, 1024);"
        # self.base_b = BPF(text=bpf_map_create_command)
        self._map_name = map_name
        self._bpf_func_list: List[Function] = []
        self._bpf_header_list: List[str] = []

    def add_bpf_function(self, bpf_func: Function):
        self._bpf_func_list.append(bpf_func)
        self._bpf_header_list.extend(bpf_func.header_list)

    def render(self) -> str:
        program = ""
        start_index = 0
        for func in self._bpf_func_list:
            program += BPFService._fun_to_bpf(func, start_index)
            start_index += func.no_obs - 1
        return BPFService._prog_to_bpf(set(self._bpf_header_list), program)

    @staticmethod
    def _fun_to_bpf(func: Function, start_index: int) -> str:
        # Environment(extensions=["jinja2.ext.do", ])
        template = Template(BPFTemplate.BPF_FUN_TEMPLATE)
        return template.render(function=func, start_index=start_index)

    @staticmethod
    def _prog_to_bpf(header_list: Set[str], prog: str) -> str:
        # Environment(extensions=["jinja2.ext.do", ])
        template = Template(BPFTemplate.BPF_PROG_TEMPLATE)
        return template.render(headers=header_list, prog=prog)
