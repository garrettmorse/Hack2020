from collections import OrderedDict
from typing import List


class VariableSymbol:
    def __init__(self, name: str):
        self.name = name


class FunctionSymbol:
    def __init__(self, name: str, parameter_names: List[str]):
        self.name = name
        self.parameters = OrderedDict()
        for name in parameter_names:
            self.parameters[name] = VariableSymbol(name)
