from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_variable() -> None:
    tokens = "a".split()
    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("a")

    assert engine.parse_expression(code) == "a"


def test_variable_thirteen() -> None:
    tokens = "thirteen".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "13"


def test_variable_thirteen_foo() -> None:
    tokens = "thirteen foo".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "13"
    assert engine.tokens == ["foo"]


def test_variable_foo_txt_twelve() -> None:
    tokens = "foo dot txt twelve".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_expression(code) == "'foo.txt'"
    assert engine.tokens == ["twelve"]


def test_variable_txt_twelve() -> None:
    tokens = "txt twelve".split()
    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("txt")

    assert engine.parse_variable(code) == "txt"
    assert engine.tokens == ["twelve"]


def test_variable_txt_twelve() -> None:
    tokens = "txt twelve".split()
    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_variable(code) == "txt"
    assert engine.tokens == ["twelve"]


def test_variable_foo_twelve() -> None:
    tokens = "foo twelve".split()
    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("foo")

    assert engine.parse_expression(code) == "foo"
    assert engine.tokens == ["twelve"]


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
    code.symbols.add_variable_symbol("file")

    assert engine.parse_expression(code) == "file.read"
    assert engine.tokens == []


def test_multi_word_expression_with_dot() -> None:
    tokens = "my file dot read".split()
    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("my_file")

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
