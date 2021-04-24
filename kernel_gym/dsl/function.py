from __future__ import annotations
from typing import List, Optional


class Function(object):

    def __init__(self, function_name: str):
        self._function_name: str = function_name
        self._arg_observer_list: List[Argument] = []
        self._header_list: List[str] = []
        self.no_obs = 1

    @property
    def function_name(self) -> str:
        return self._function_name

    @property
    def arg_observer_list(self) -> List[Argument]:
        return self._arg_observer_list

    @property
    def header_list(self) -> List[str]:
        return self._header_list

    def arg(self, arg_type: str, arg_name: str) -> Argument:
        argument = Argument(self, arg_type, arg_name)
        self._arg_observer_list.append(argument)
        return argument

    def header(self, header_file_name: str) -> Function:
        self._header_list.append(header_file_name)
        return self


class Argument(object):

    def __init__(self, f: Function, arg_type: str, arg_name: str):
        self._f = f
        self._arg_type = arg_type
        self._arg_name = arg_name
        self._extractor_list: List[Extractor] = []

    @property
    def arg_type(self):
        return self._arg_type

    @property
    def arg_name(self):
        return self._arg_name

    @property
    def extractor_list(self):
        return self._extractor_list

    def extract(self, prop: str = None, rescale_low: int = None, rescale_high: int = None) -> Argument:
        if prop is None:
            return self
        extractor: Extractor = Extractor(prop, rescale_low, rescale_high)
        self._extractor_list.append(extractor)
        self._f.no_obs = self._f.no_obs + 1
        return self

    def next(self) -> Function:
        """

        @rtype: object
        """
        return self._f


class Extractor(object):

    def __init__(self, prop: str, rescale_low: Optional[int] = None, rescale_high: Optional[int] = None):
        self._prop: str = prop
        self._rescale_low: Optional[int] = rescale_low
        self._rescale_high: Optional[int] = rescale_high

    @property
    def prop(self):
        return self._prop

    @property
    def rescale_low(self):
        return self._rescale_low

    @property
    def rescale_high(self):
        return self._rescale_high
