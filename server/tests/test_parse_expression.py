from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_variable() -> None:
    tokens = "a".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "a"


def test_addition() -> None:
    tokens = "a plus b".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "a + b"
    assert engine.tokens == []


def test_subtraction() -> None:
    tokens = "a minus b".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "a - b"
    assert engine.tokens == []


def test_multiplication() -> None:
    tokens = "a times b".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "a * b"
    assert engine.tokens == []


def test_multi_word_variable() -> None:
    tokens = "line count times n".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_variable(code) == "line_count"
    assert engine.tokens == "times n".split()


def test_multi_word_variable_with_double_word_op() -> None:
    tokens = "line count less than n".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_variable(code) == "line_count"
    assert engine.tokens == "less_than n".split()


def test_two_multi_word_variable() -> None:
    tokens = "line count times file size".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "line_count * file_size"
    assert engine.tokens == []


def test_expression_with_dot() -> None:
    tokens = "file dot read".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "file.read"
    assert engine.tokens == []


def test_multi_word_expression_with_dot() -> None:
    tokens = "my file dot read".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "my_file.read"
    assert engine.tokens == []


def test_multi_word_expression_with_dot() -> None:
    tokens = "my file dot read".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "my_file.read"
    assert engine.tokens == []


def test_multi_word_op() -> None:
    tokens = "x less than y".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "x < y"
    assert engine.tokens == []


def test_multi_word_op_and_var() -> None:
    tokens = "line count times file size less than total space".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "line_count * file_size < total_space"
    assert engine.tokens == []
