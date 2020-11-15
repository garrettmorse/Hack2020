import enum
from typing import List


class PrimaryKeywords(enum.Enum):
    FUNCTION = "function"
    CALL = "call"
    RETURN = "return"
    IF = "if"
    ELSE = "else"
    SET = "set"
    APPEND = "append"
    PREPEND = "prepend"
    FOR = "for"
    TABOUT = "tabout"
    GOTO = "goto"
    DELETE = "delete"

    @staticmethod
    def values() -> List[str]:
        return [e.value for e in PrimaryKeywords]


class SecondaryKeywords(enum.Enum):
    ARGUMENT = "argument"
    PLUS = "plus"
    MINUS = "minus"
    TIMES = "times"
    DOT = "dot"
    DIVIDE = "divide"
    THEN = "then"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    GREATER_THAN_OR_EQUAL_TO = "greater_than_or_equal_to"
    LESS_THAN_OR_EQUAL_TO = "less_than_or_equal_to"
    EQUALS = "equals"
    AND = "and"
    OR = "or"
    TO = "to"
    RANGE = "range"
    IN = "in"
    MODULO = "modulo"

    @staticmethod
    def values() -> List[str]:
        return [e.value for e in SecondaryKeywords]
