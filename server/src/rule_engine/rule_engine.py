import sys
from typing import List
from .keywords import PrimaryKeywords, SecondaryKeywords


class Symbol:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class RuleEngine:
    def __init__(self):
        # TODO: Dict of something
        self.symbols = {}
        self.nums = {"one": 1,
                     "two": 2,
                     "three": 3,
                     "four": 4,
                     "five": 5,
                     "six": 6,
                     "seven": 7,
                     "eight": 8,
                     "nine": 9,
                     "ten": 10
                     }

    def parse(self, text: str):
        tokens = text.strip().split(" ")

        parsed_tokens = []
        for token in tokens:
            lowercase_token = token.lower()
            if lowercase_token in PrimaryKeywords:
                parsed_tokens.append(PrimaryKeywords[token])
            elif lowercase_token in SecondaryKeywords:
                parsed_tokens.append(SecondaryKeywords[token])
            else:
                parsed_tokens.append(token)

        return self.parse_core(tokens)

    def parse_core(self, tokens):
        first = tokens[0]
        if first in PrimaryKeywords:
            return getattr(self, f"parse_{first.value}")(tokens)
        else:
            print("NOT IMPLEMENTED EXCEPTION")

    def _build_func_definition(name: str, params: List[str]) -> str:
        paramstr = ", ".join(params)
        return f"def {name}({paramstr}):\n"

    def parse_function(self, tokens: List[str]):
        arg_i = -1
        and_i = -1  # Assume only 1 "and" per definition
        for i, t in enumerate(tokens):
            if t == "argument" or t == "arguments":
                arg_i = i
            if t == "and":
                and_i = i

        num_args = self.nums[tokens[arg_i-1]]
        params = ["" for i in range(num_args)]
        func_name = "_".join(tokens[1:arg_i-2])
        if and_i != -1:
            params[-1] = " ".join(tokens[and_i:])
            tokens = tokens[:and_i]
            num_args = num_args - 1
        tokens = tokens[arg_i + 1:]
        for j in range(num_args-1):
            params[j] = tokens[j]
        params[j] = tokens[j:].join("_")
        return _build_func_definition(func_name, params)

    def parse_call(self, tokens):
        pass

    def parse_return(self, tokens):
        pass

    def parse_then(self, tokens):
        pass

    def parse_if(self, tokens):
        pass

    def parse_else(self, tokens):
        pass

    def parse_set(self, tokens):
        pass

    def parse_append(self, tokens):
        pass

    def parse_prepend(self, tokens):
        pass

    def parse_for(self, tokens):
        pass
