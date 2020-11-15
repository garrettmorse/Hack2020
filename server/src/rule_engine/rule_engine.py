from typing import Callable, Dict, Iterable, List, Optional, Tuple

from src.state_engine.code import Line
from typing_extensions import Literal

import copy
from ..state_engine import Code
from . import utils
from .keywords import PrimaryKeywords, SecondaryKeywords

ParseFunc = Callable[[Code], Optional[str]]


class RuleEngine:
    tokens: List[str]

    def __init__(self, tokens: Iterable[str] = []) -> None:
        self.tokens = []
        self.add_tokens(tokens)

    @classmethod
    def find_next(
        self, tokens: Iterable[str], *containers: Iterable[str]
    ) -> Tuple[int, Optional[str]]:
        for index, token in enumerate(tokens):
            for container in containers:
                if token in container:
                    return index, token
        return -1, None

    @classmethod
    def find_next_specific(self, tokens: Iterable[str], token_specific: str):
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
        transforms = {  # order is important
            "arguments": "argument",
            "greater than or equal to": "greater_than_or_equal_to",
            "less than or equal to": "less_than_or_equal_to",
            "greater than": "greater_than",
            "less than": "less_than",
            "go to": "goto",
        }

        body = " ".join(tokens).lower()

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

    def popmany(self, i: int) -> None:
        for _ in range(i):
            self.pop()

    def check_next(self, tok: str) -> None:
        assert self.peek() == tok, f"next token '{self.peek()}' is not '{tok}'"

    def putback(self, tokens: List[str]) -> None:
        self.tokens = tokens + self.tokens

    def parse(self, code: Code) -> Code:
        """
        Consumes tokens from self.tokens and returns a new Code with additional lines.
        """

        # based on first token in self.tokens, do something different
        parse_fns: Dict[str, ParseFunc] = {
            "for": self.parse_for,
            "if": self.parse_if,
            "else": self.parse_else,
            "set": self.parse_set,
            "function": self.parse_function,
            "call": self.parse_call,
            "append": self.parse_append,
            "prepend": self.parse_prepend,
            "return": self.parse_return,
            "tabout": self.parse_tabout,
            "remove": self.parse_delete,
            "goto": self.parse_goto,
        }

        while self.tokens and self.peek() in parse_fns:
            spec = self.peek()
            parsed_line = parse_fns[self.peek()](code)
            if spec != "goto" and spec != "delete":
                code.add_line(parsed_line)

        return copy.deepcopy(code)

    def parse_tabout(self, code: Code) -> str:
        self.check_next("tabout")
        self.pop()
        code.add_line(" ", tab_out_number=1)
        return " "

    def parse_function(self, code: Code) -> str:
        self.check_next("function")
        self.pop()
        tokens = self.tokens

        arg_i = self.tokens.index("argument")
        stop_i, _ = self.find_next(self.tokens, PrimaryKeywords.values())
        if stop_i < 0:
            stop_i = len(self.tokens)
        and_i, _ = self.find_next_specific(tokens, "and")

        num_args = utils.text2int(tokens[arg_i - 1])
        params = ["" for i in range(num_args)]
        func_name = "_".join(tokens[: arg_i - 1])

        last_param = ""
        if and_i != -1:
            last_param = "_".join(tokens[and_i + 1 : stop_i])

        if num_args == 1:
            params = ["_".join(tokens[arg_i + 1 : stop_i])]
        elif num_args > 0:
            params = tokens[arg_i + 1 : arg_i + num_args - 1]

            if and_i < 0:
                and_i = stop_i
            params.append("_".join(tokens[arg_i + num_args - 1 : and_i]))

        if last_param:
            params.append(last_param)

        code.symbols.add_function_symbol(func_name, *params)

        paramstr = ", ".join(params)
        self.tokens = tokens[stop_i:]
        return f"def {func_name}({paramstr}):"

    def parse_call(self, code: Code) -> str:
        """
        CALL print file length times file size
        """
        self.check_next("call")
        self.pop()
        func_name = self.parse_variable(code, context="function")
        if func_name not in code.symbols.function_symbols:
            self.putback(func_name.split("_"))
            func_name = self.pop()

            stop_i, _ = self.find_next(self.tokens, PrimaryKeywords.values())
            if stop_i < 0:
                stop_i = len(self.tokens)

            params = self.tokens[:stop_i]

            num_params = len(params)
            self.popmany(num_params)
        else:
            func_symbol = code.symbols.function_symbols[func_name]
            num_params = len(func_symbol.parameters)

            params = []
            for i in range(num_params):
                params.append(self.parse_expression(code))

        param_str = ", ".join(params)
        return f"{func_name}({param_str})"

    def parse_return(self, code: Code) -> str:
        self.check_next("return")
        self.pop()
        expr = self.parse_expression(code)
        return f"return {expr}"

    def parse_if(self, code: Code) -> str:
        """
        IF boolean expression THEN action
        """
        self.check_next("if")
        self.pop()

        expr = self.parse_expression(code)

        self.check_next("then")
        self.pop()

        return f"if {expr}:"

    def parse_else(self, code: Code) -> str:
        """
        ELSE action
        """
        self.check_next("else")
        self.pop()
        return "else:"

    def parse_set(self, code: Code) -> str:
        """
        SET x to y
        """
        self.check_next("set")
        self.pop()
        name = self.parse_variable(code)

        self.check_next("to")
        self.pop()
        expr = self.parse_expression(code)

        code.symbols.add_variable_symbol(name)

        return f"{name} = {expr}"

    def parse_append(self, code: Code) -> str:
        """
        APPEND result TO product list
        """
        assert self.peek() == "append"
        self.pop()

        ele = self.parse_expression(code)

        assert self.peek() == "to"
        self.pop()

        col = self.parse_variable(code, context="variable")
        return f"{col}.append({ele})"

    def parse_prepend(self, code: Code) -> str:
        """
        PREPEND result TO product list
        """
        assert self.peek() == "prepend"
        self.pop()

        ele = self.parse_expression(code)

        assert self.peek() == "to"
        self.pop()

        col = self.parse_variable(code, context="variable")
        return f"{col}.insert(0, {ele})"

    def parse_for(self, code: Code) -> str:
        """
        FOR var IN collection

        collection that starts with keyword RANGE signals integer range.

        FOR var IN RANGE num1 TO num2
        """
        assert self.peek() == "for"
        self.pop()

        iter_var = self.parse_variable(code, context="variable")

        assert self.peek() == "in"
        self.pop()

        if self.peek() == "range":
            self.pop()
            r1 = self.parse_expression(code)

            assert self.peek() == "to"
            self.pop()
            r2 = self.parse_expression(code)

            return f"for {iter_var} in range({r1}, {r2}):"
        else:
            col = self.parse_variable(code, context="variable")
            return f"for {iter_var} in {col}:"

    def parse_expression(self, code: Code) -> str:

        expression: List[str] = []

        ops = {
            "times": "*",
            "plus": "+",
            "minus": "-",
            "modulo": "%",
            "greater_than": ">",
            "greater_than_or_equal_to": ">=",
            "less_than_or_equal_to": "<=",
            "less_than": "<",
            "equals": "==",
            "and": "and",
        }

        if self.peek() == "call":
            expression.append(self.parse_call(code))
        else:
            expression.append(self.parse_variable(code))

        if self.tokens and self.peek() == "dot":
            self.pop()  # discard .
            obj = expression[0]
            method = self.parse_variable(code)

            if obj in code.symbols.variable_symbols:
                left = f"{obj}.{method}"
            else:
                return f"'{obj}.{method}'"
        else:
            left = " ".join(expression)

        if self.tokens and self.peek() in ops:
            op = ops[self.pop()]
            right = self.parse_expression(code)

            return " ".join([left, op, right])
        else:
            return left

    def parse_variable(
        self, code: Code, context: Literal["function", "variable"] = "variable"
    ) -> str:

        if context == "function":
            fn_match = code.symbols.find_best_matching_function_symbol(self.tokens)
            if fn_match:
                fn_symbol, consumed = fn_match
                self.popmany(consumed)
                return fn_symbol.name
        else:
            var_match = code.symbols.find_best_matching_variable_symbol(self.tokens)
            if var_match:
                var_symbol, consumed = var_match
                self.popmany(consumed)
                return var_symbol.name

        # variable not found in symbol table

        variable = []

        keywords = PrimaryKeywords.values() + SecondaryKeywords.values()

        while self.tokens and (self.peek() not in keywords):
            variable.append(self.pop())

        if not variable:
            return ""

        for i, chunk in enumerate(variable):
            success, num = utils.safe_text2int(chunk)
            if success:
                break
        else:
            return "_".join(variable)

        if i == 0:
            self.putback(variable[i + 1 :])
            return str(num)
        else:
            self.putback(variable[i:])
            return "_".join(variable[:i])

    def parse_goto(self, code: Code) -> None:
        """
        GOTO line 58

        GOTO line END

        GOTO line BEGINNING
        """
        self.check_next("goto")
        self.pop()
        self.check_next("line")
        self.pop()

        if self.peek() == "end":
            self.pop()
            code.set_cursor_to_end()
        elif self.peek() == "beginning":
            self.pop()
            code.set_cursor_to_beginning()
        else:
            line_num = self.parse_variable(code)
            code.set_cursor(int(line_num))

    def parse_delete(self, code: Code) -> None:
        """
        Remove line 58

        Remove line END
        """
        assert self.peek() == "remove"
        self.pop()
        self.check_next("line")
        self.pop()

        if self.peek() == "end":
            self.pop()
            code.delete_last_line()
        elif self.peek() == "beginning":
            self.pop()
            code.delete_first_line()
        else:
            line_num = self.parse_variable(code)
            code.delete_line(int(line_num))
