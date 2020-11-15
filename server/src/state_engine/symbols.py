from collections import OrderedDict
from typing import List


class Symbols:
    def __init__(self) -> None:
        self.variable_symbols: List[VariableSymbol] = []
        self.function_symbols: List[FunctionSymbol] = []

    def add_function_symbol(self, function_name: str, *parameter_names: str) -> None:
        self.function_symbols.append(
            FunctionSymbol(function_name, list(parameter_names))
        )

    def add_variable_symbol(self, variable_name: str) -> None:
        self.variable_symbols.append(VariableSymbol(variable_name))


class VariableSymbol:
    def __init__(self, variable_name: str) -> None:
        self.name = variable_name


class FunctionSymbol:
    def __init__(self, function_name: str, parameter_names: List[str]) -> None:
        self.name = function_name
        self.parameters = OrderedDict()
        for name in parameter_names:
            self.parameters[name] = VariableSymbol(name)
