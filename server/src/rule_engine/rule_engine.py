from typing import Callable, Dict, Iterable, List

from ..state_engine import Code
from .keywords import PrimaryKeywords, SecondaryKeywords
from .symbol import Symbol

ParseFunc = Callable[[Code], str]


class RuleEngine:
    tokens: List[str]
    code: Code

    def __init__(self, tokens: Iterable[str] = []) -> None:
        self.tokens = []
        # TODO: Dict of something
        self.symbols = {}
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
        self.add_tokens(tokens)

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
    def consume_many(self, tokens, number):
        return tokens[1 + number :]

    def add_tokens(self, tokens: Iterable[str]) -> None:
        transforms = {
            "greater than": "greater_than",
            "less than": "less_than",
            "greater than or equal to": "greater_than_or_equal_to",
        }

        body = " ".join(tokens)

        for dirty, clean in transforms.items():
            body = body.replace(dirty, clean)

        self.tokens += list(body.split())

    def peek(self) -> str:
        assert len(self.tokens) >= 1, f"called peek with {self.tokens}"
        return self.tokens[0]

    def peekpeek(self) -> str:
        assert len(self.tokens) >= 2, f"called peekpeek with {self.tokens}"
        return self.tokens[1]

    def pop(self) -> str:
        top = self.tokens[0]
        self.tokens = self.tokens[1:]
        return top

    def parse(self, code: Code) -> Code:
        """
        Consumes tokens from self.tokens and returns a new Code with additional lines.
        """

        # based on first token in self.tokens, do something different
        parse_fns: Dict[str, ParseFunc] = {
            "for": self.parse_for,
            "if": self.parse_if,
            "set": self.parse_set,
            "function": self.parse_function,
            "call": self.parse_call,
            "append": self.parse_append,
            "prepend": self.parse_prepend,
        }

        while self.peek() in parse_fns:
            parsed_line = parse_fns[self.pop()](self.code)
            self.code.add_line(parsed_line)

        return self.code

    def _build_func_definition(self, name: str, params: List[str]) -> str:
        paramstr = ", ".join(params)
        return f"def {name}({paramstr}):\n"

    def parse_function(self, tokens: List[str]) -> List[str]:
        arg_i, _ = self.find_next_specific(tokens, SecondaryKeywords.ARGUMENT)
        and_i, _ = self.find_next_specific(tokens, SecondaryKeywords.AND)
        num_args = self.nums[tokens[arg_i - 1]]
        params = ["" for i in range(num_args)]
        func_name = "_".join(tokens[1 : arg_i - 2])
        if and_i != -1:
            params[-1] = " ".join(tokens[and_i:])
            tokens = tokens[:and_i]
            num_args = num_args - 1
        tokens = tokens[arg_i + 1 :]
        for j in range(num_args - 1):
            params[j] = tokens[j]
        params[j] = tokens[j:].join("_")

        self.symbols[func_name] = Symbol(
            func_name, {"type": "function", "params": params, "num_params": len(params)}
        )

        return [self._build_func_definition(func_name, params)]

    def parse_call(self, code: Code) -> str:
        raise NotImplementedError()

    def parse_return(self, tokens):
        return f"return {self.parse_core(tokens)}\n"

    def parse_if(self, tokens: List[str]) -> List[str]:
        """
        IF boolean expression THEN action .../ELSE boolean expressions THEN action
        """
        code_rep = []
        tokens = tokens[1:]
        then_i, _ = self.find_next_specific(tokens, SecondaryKeywords.THEN)
        expr_tokens = tokens[:then_i]
        expr_str = self.parse_core(expr_tokens)
        code_rep.append(f"if {expr_str}:\n")
        tokens = tokens[then_i + 1 :]

        else_i, _ = self.find_next_specific(tokens, PrimaryKeywords.ELSE)
        if else_i == -1:
            code_rep.append("\t" + self.parse_core(tokens))
            tokens = []
        else:
            code_rep.append("\t" + self.parse_core(tokens[:else_i]))
            tokens = tokens[else_i + 1 :]

        while not self.is_EOS(tokens):
            then_i, _ = self.find_next_specific(tokens, SecondaryKeywords.THEN)
            # Assume final else: ELSE THEN action
            expr_tokens = tokens[:then_i]
            if tokens:
                expr_str = self.parse_core(expr_tokens)
                code_rep.append(f"else {expr_str}:\n")
            else:
                code_rep.append("else:\n")

            tokens = tokens[then_i + 1 :]
            else_i, _ = self.find_next_specific(tokens, PrimaryKeywords.ELSE)
            if else_i == -1:
                code_rep.append("\t" + self.parse_core(tokens))
                tokens = []
            else:
                code_rep.append("\t" + self.parse_core(tokens[:else_i]))
                tokens = tokens[else_i + 1 :]

        return code_rep

    def parse_set(self, tokens: List[str]) -> List[str]:
        """
        SET x to y
        """
        code_rep = []
        to_i, _ = self.find_next_specific(tokens, SecondaryKeywords.TO)
        name = "_".join(tokens[1:to_i])
        tokens = RuleEngine.consume_many(tokens, to_i)
        expr = self.parse_core(tokens)
        code_rep.append(f"{name}={expr}\n")
        self.symbols[name] = Symbol(name, expr)
        return code_rep

    def parse_append(self, tokens):
        """
        APPEND result TO product list
        """
        code_rep = []
        to_i, _ = self.find_next_specific(tokens, SecondaryKeywords.TO)
        # Might use the symbols here witha  find_best_match function
        try_ele = "_".join(tokens[1:to_i])
        col = "_".join(tokens[to_i + 1 :])
        code_rep.append(f"{col}.append({try_ele})")
        # May have to update symbols with updated value
        return code_rep

    def parse_prepend(self, tokens):
        """
        PREPEND result TO product list
        """
        code_rep = []
        to_i, _ = self.find_next_specific(tokens, SecondaryKeywords.TO)
        # Might use the symbols here witha  find_best_match function
        try_ele = "_".join(tokens[1:to_i])
        col = "_".join(tokens[to_i + 1 :])
        code_rep.append(f"{col}.insert(0, {try_ele})")
        # May have to update symbols with updated value
        return code_rep

    def parse_for(self, tokens):
        """
        FOR var IN collection

        collection that starts with keyword RANGE signals integer range.

        FOR var IN RANGE num1 TO num2
        """

        code_rep = []
        in_i, _ = self.find_next_specific(tokens, SecondaryKeywords.IN)
        iter_var = "_".join(tokens[1:in_i])
        # iter_var = find_best_match(iter_var)
        self.symbols[iter_var] = Symbol(iter_var, {"type": "literator"})
        range_i, _ = self.find_next_specific(tokens, SecondaryKeywords.RANGE)
        if range_i != -1:
            # collection is a numerical range
            to_i, _ = self.find_next_specific(tokens, SecondaryKeywords.TO)
            x1 = "_".join(tokens[range_i + 1 : to_i])
            x2 = "_".join(tokens[to_i + 1 :])
            """
            x1 = find_best_match(x1)
            x2 = find_best_match(x2)
            """
            code_rep.append(f"for {iter_var} in range({x1}, {x2}):\n")
        else:
            col = "_".join(tokens[in_i + 1 :])
            # col = find_best_match(col)
            code_rep.append(f"for {iter_var} in {col}:\n")
        return code_rep

    def parse_expression(self, code: Code) -> str:
        expression: List[str] = []

        ops = {
            "times": "*",
            "plus": "+",
            "minus": "-",
            "greater_than": ">",
            "less_than": "<",
        }

        expression.append(self.parse_variable(code))

        if self.tokens and self.peek() in ops:
            expression.append(ops[self.pop()])
            expression.append(self.parse_expression(code))
        elif self.tokens and self.peek() == "dot":
            self.pop()  # discard .
            expression[-1] += "." + self.parse_variable(code)

        return " ".join(expression)

    def parse_variable(self, code: Code) -> str:
        variable = []

        keywords = PrimaryKeywords.list_values() + SecondaryKeywords.list_values()

        while self.tokens and (self.peek() not in keywords):
            variable.append(self.pop())

        return "_".join(variable)
