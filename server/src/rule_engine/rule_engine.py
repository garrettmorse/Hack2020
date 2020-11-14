import os
import sys


class RuleEngine:
    def __init__(self):
        pass

    def parse_wrapper(self, text: str):
        tokens = text.split()
        return self.parse(tokens)

    def parse(self, tokens):
        # Other work here

        result = ""
        return result

    def parse_function(self, tokens):
        pass

    def parse_argument(self, tokens):
        pass

    def parse_call(self, tokens):
        pass

    def parse_return(self, tokens):
        pass

    def parse_plus(self, tokens):
        pass

    def parse_minus(self, tokens):
        pass

    def parse_times(self, tokens):
        pass

    def parse_dot(self, tokens):
        pass

    def parse_divide(self, tokens):
        pass

    def parse_then(self, tokens):
        pass

    def parse_greater_than(self, tokens):
        pass

    def parse_less_than(self, tokens):
        pass

    def parse_greater_than_or_equal_to(self, tokens):
        pass

    def parse_less_than_or_equal_to(self, tokens):
        pass


# PLUS = "plus"
# MINUS = "minus"
# TIMES = "times"
# DOT = "dot"
# DIVIDE = "divide"
# THEN = "then"
# GREATER_THAN = "greater_than"
# LESS_THAN = "less_than"
# GREATER_THAN_OR_EQUAL_TO = "greater_than_or_equal_to"
# LESS_THAN_OR_EQUAL_TO = "less_than_or_equal_to"
# IF = "if"
# ELSE = "else"
# SET = "set"
# EQUALS = "equals"
# AND = "and"
# OR = "or"
# APPEND = "append"
# PREPEND = "prepend"
# FOR = "for"