from collections import OrderedDict
from typing import Dict, Iterator, List, Optional, Tuple


class VariableSymbol:
    def __init__(self, variable_name: str) -> None:
        self.name = variable_name


class FunctionSymbol:
    def __init__(self, function_name: str, parameter_names: List[str]) -> None:
        self.name = function_name
        self.parameters = OrderedDict()
        for name in parameter_names:
            self.parameters[name] = VariableSymbol(name)


class Symbols:
    def __init__(self) -> None:
        self.function_symbols: Dict[str, FunctionSymbol] = {}
        self.variable_symbols: Dict[str, VariableSymbol] = {}

    def add_function_symbol(self, function_name: str, *parameter_names: str) -> None:
        self.function_symbols[function_name] = FunctionSymbol(
            function_name, list(parameter_names)
        )

    def add_variable_symbol(self, variable_name: str) -> None:
        self.variable_symbols[variable_name] = VariableSymbol(variable_name)

    def find_best_matching_function_symbol(
        self, tokens: List[str]
    ) -> Optional[Tuple[FunctionSymbol, int]]:
        for option, num_used in self.generate_symbol_token_match_options(tokens):
            if option in self.function_symbols:
                return (self.function_symbols[option], num_used)
        return None

    def find_best_matching_variable_symbol(
        self, tokens: List[str]
    ) -> Optional[Tuple[VariableSymbol, int]]:
        for option, num_used in self.generate_symbol_token_match_options(tokens):
            if option in self.variable_symbols:
                return (self.variable_symbols[option], num_used)
        return None

    @staticmethod
    def generate_symbol_token_match_options(
        tokens: List[str],
    ) -> Iterator[Tuple[str, int]]:
        pos = 0
        while pos < len(tokens):
            token_list = tokens[: pos + 1]
            if len(token_list) > 1:
                yield ("_".join(token_list), pos + 1)
            yield ("".join(token_list), pos + 1)
            yield ("".join([token.capitalize() for token in token_list]), pos + 1)
            pos += 1
