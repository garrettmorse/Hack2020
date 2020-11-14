import sys
from .keywords import PrimaryKeywords, SecondaryKeywords


class RuleEngine:
    def __init__(self):
        # TODO: Dict of something
        self.symbols = {}

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
    def consume(self, tokens):
        return tokens[1:]

    @classmethod
    def consume_many(self, tokens, number):
        return tokens[1 + number :]

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

    def parse_function(self, tokens):
        pass

    def parse_call(self, tokens):
        pass

    def parse_return(self, tokens):
        return f"return {self.parse_core(tokens)}\n"

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