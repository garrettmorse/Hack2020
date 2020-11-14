import enum


class PrimaryKeywords(enum.Enum):
    FUNCTION = "function"
    CALL = "call"
    RETURN = "return"
    THEN = "then"
    IF = "if"
    ELSE = "else"
    SET = "set"
    APPEND = "append"
    PREPEND = "prepend"
    FOR = "for"

    @staticmethod
    def list_keys():
        return list(map(lambda e: e.key, PrimaryKeywords))

    @staticmethod
    def list_values():
        return list(map(lambda e: e.value, PrimaryKeywords))


class SecondaryKeywords(enum.Enum):
    ARGUMENT = "argument"
    ARGUMENTS = "arguments"
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

    @staticmethod
    def list_keys():
        return list(map(lambda e: e.key, SecondaryKeywords))

    @staticmethod
    def list_values():
        return list(map(lambda e: e.value, SecondaryKeywords))