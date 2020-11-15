from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_main_func() -> None:
    tokens = ["function", "main", "zero", "arguments"]

    code = Code()
    engine = RuleEngine()
    engine.add_tokens(tokens)

    assert engine.parse_function(code) == "def main():"
    assert engine.tokens == "".split()


def test_basic_func() -> None:
    tokens = "function f two arguments a and b".split()

    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_function(code) == "def f(a, b):"
    assert engine.tokens == "".split()


def test_func_zero_args() -> None:
    tokens = "function f zero arguments".split()

    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_function(code) == "def f():"
    assert engine.tokens == "".split()


def test_multi_word_func_one_arg() -> None:
    tokens = "function read file one argument name".split()

    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_function(code) == "def read_file(name):"
    assert engine.tokens == "".split()


def test_multi_word_func_one_multi_word_arg() -> None:
    tokens = "function read file one argument file location".split()

    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_function(code) == "def read_file(file_location):"
    assert engine.tokens == "".split()

def test_base() -> None:
    tokens = "function main zero arguments".split()

    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_function(code) == "def main():"
    assert engine.tokens == "".split()
