import sys
from typing import List, Any

from typing_extensions import final
from .keywords import PrimaryKeywords, SecondaryKeywords
from .symbol import Symbol
from ..state_engine import Code, Line


class RuleEngine:
    def __init__(self):
        self.symbols = {}
        self.tokens = []
        self.nums = {
            "zero": 0,
            "one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10,
        }

    @classmethod
    def find_next(self, tokens, *containers):
        for index, token in enumerate(tokens):
            for container in containers:
                if token in container:
                    return index, token
        return -1, None

    @classmethod
    def find_next_specific(self, tokens, token_specific):
        for index, token in enumerate(tokens):
            if token == token_specific:
                return index, token
        return -1, None

    @classmethod
    def is_EOS(self, tokens):
        if not tokens or len(tokens) == 0:
            return True
        else:
            return False

    @classmethod
    def is_last(self, tokens):
        if not tokens:
            return False
        elif len(tokens) == 1:
            return True
        else:
            return False

    @classmethod
    def consume(self):
        return self.tokens[1:]

    @classmethod
    def consume_many(self, tokens, number):
        return tokens[1 + number:]

    def parse(self, code: Code, text: str) -> Code:
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

        self.parse_core(parsed_tokens, code)
        return code

    def parse_core(self, tokens: List[Any], code: Code) -> Code:
        first = tokens[0]
        if first in PrimaryKeywords:
            code_str = getattr(self, f"parse_{first.value}")(tokens)
        else:
            print("NOT IMPLEMENTED EXCEPTION")

        code.add_line(code_str)
        return code

    def parse_expression(self, tokens: List[str], code: Code):
        pass

    def parse_function(self, code: Code) -> str:
        tokens = self.tokens[1:]
        arg_i, _ = self.find_next_specific(tokens, SecondaryKeywords.ARGUMENT)
        stop_i, _ = self.find_next(tokens, PrimaryKeywords)

        and_i, _ = self.find_next_specific(tokens, SecondaryKeywords.AND)

        num_args = self.nums[tokens[arg_i - 1]]
        params = ["" for i in range(num_args)]
        func_name = "_".join(tokens[:arg_i - 1])
        if and_i != -1:
            params[-1] = "_".join(tokens[and_i + 1:stop_i])
            num_args = num_args - 1

        param_tokens = tokens[:and_i]
        i = 0
        while i < num_args - 1:
            params[i] = param_tokens[i]
            i += 1
        params[i] = "_".join(param_tokens[i:])

        # self.symbols[func_name] = Symbol() TODO when symbols get defined

        paramstr = ", ".join(params)
        self.tokens = tokens[stop_i:]
        return f"def {func_name}({paramstr}):\n"

    def parse_call(self, code: Code) -> str:
        tokens = self.tokens
        # TODO when symbols are defined.
        pass

    def parse_return(self, code: Code) -> str:
        self.tokens = self.tokens[1:]
        expr = self.parse_expression(code)
        return f"return {expr}\n"

    def parse_if(self, code: Code) -> str:
        """
        IF boolean expression THEN action
        """
        tokens = self.tokens[1:]

        self.tokens = tokens
        expr = self.parse_expression(code)
        tokens = self.tokens
        then_i, _ = self.find_next_specific(tokens, SecondaryKeywords.THEN)
        self.tokens = tokens[then_i + 1:]
        return f"if {expr}:"

    def parse_else(self, code: Code) -> str:
        """
        ELSE action
        """
        tokens = self.tokens[1:]
        self.tokens = tokens
        return f"else:"

    def parse_set(self, code: Code) -> str:
        """
        SET x to y
        """
        tokens = self.tokens[1:]
        to_i, _ = self.find_next_specific(tokens, SecondaryKeywords.TO)
        name = "_".join(tokens[:to_i])

        self.tokens = tokens[to_i + 1:]
        expr = self.parse_expression(code)

        # Update Symbols TODO

        return f"{name} = {expr}"

    def parse_append(self, code: Code) -> str:
        """
        APPEND result TO product list
        """
        tokens = self.tokens[1:]
        to_i, _ = self.find_next_specific(tokens, SecondaryKeywords.TO)
        stop_i, _ = self.find_next(tokens, PrimaryKeywords)
        # Might use the symbols here witha  find_best_match function
        try_ele = "_".join(tokens[:to_i])
        col = "_".join(tokens[to_i + 1:stop_i])

        self.tokens = tokens[stop_i:]
        # TODO update symbols?
        return f"{col}.append({try_ele})"

    def parse_prepend(self, code: Code) -> str:
        """
        PREPEND result TO product list
        """
        tokens = self.tokens[1:]
        to_i, _ = self.find_next_specific(tokens, SecondaryKeywords.TO)
        stop_i, _ = self.find_next(tokens, PrimaryKeywords)
        # Might use the symbols here witha  find_best_match function
        try_ele = "_".join(tokens[:to_i])
        col = "_".join(tokens[to_i + 1:stop_i])

        self.tokens = tokens[stop_i:]
        # TODO update symbols?
        return f"{col}.insert(0, {try_ele})"

    def parse_for(self, code: Code) -> str:
        """
        FOR var IN collection

        collection that starts with keyword RANGE signals integer range.

        FOR var IN RANGE num1 TO num2
        """
        tokens = self.tokens[1:]
        in_i, _ = self.find_next_specific(tokens, SecondaryKeywords.IN)
        stop_i, _ = self.find_next(tokens, PrimaryKeywords)

        iter_var = "_".join(tokens[:in_i])
        # iter_var = find_best_match(iter_var)
        self.symbols[iter_var] = Symbol(iter_var, {"type": "literator"})  # TODO
        range_i, _ = self.find_next_specific(tokens[:stop_i], SecondaryKeywords.RANGE)

        self.tokens = tokens[stop_i:]
        if range_i != -1:
            # collection is a numerical range
            to_i, _ = self.find_next_specific(tokens, SecondaryKeywords.TO)
            x1 = "_".join(tokens[range_i + 1: to_i])
            x2 = "_".join(tokens[to_i + 1:stop_i])
            """
            x1 = find_best_match(x1)
            x2 = find_best_match(x2)
            """
            return f"for {iter_var} in range({x1}, {x2}):\n"
        else:
            col = "_".join(tokens[in_i + 1:stop_i])
            # col = find_best_match(col)
            return f"for {iter_var} in {col}:\n"
