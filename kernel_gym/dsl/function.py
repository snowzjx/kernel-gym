from __future__ import annotations


class Function:

    def __init__(self, function_name: str):
        self._function_name: str = function_name
        self._arg_observer_list = []

    def arg(self, arg_type: str, arg_name: str) -> Argument:
        argument = Argument(self, arg_type, arg_name)
        self._arg_observer_list.append(argument)
        return argument

    def to_bpf_prog(self):
        pass


class Argument:

    def __init__(self, f: Function, arg_type: str, arg_name: str):
        self._f = f
        self._arg_type = arg_type
        self._arg_name = arg_name
        self._extracted_prop = None
        self._rescale_low = None
        self._rescale_high = None

    def extract(self, prop: str) -> Argument:
        if self._extracted_prop is not None:
            raise Exception("Only extract once is allowed...")
        self._extracted_prop = prop
        return self

    def rescale(self, low: int, high: int) -> Argument:
        if self._rescale_low is not None or self._rescale_high is not None:
            raise Exception("Only rescale once is allowed...")
        self._rescale_low = low
        self._rescale_high = high
        return self

    def next(self) -> Function:
        return self._f
