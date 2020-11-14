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

    def parse_if(self, tokens):
        pass

    def parse_else(self, tokens):
        pass

    def parse_set(self, tokens):
        pass

    def parse_equals(self, tokens):
        pass

    def parse_and(self, tokens):
        pass

    def parse_or(self, tokens):
        pass

    def parse_append(self, tokens):
        pass

    def parse_for(self, tokens):
        pass
