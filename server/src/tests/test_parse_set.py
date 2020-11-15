from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_set_basic() -> None:
    tokens = "set a to b".split()

    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("a")
    code.symbols.add_variable_symbol("b")

    assert engine.parse_set(code) == "a = b"
    assert engine.tokens == "".split()


def test_set_expr() -> None:
    tokens = "set a to b plus five".split()

    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("a")
    code.symbols.add_variable_symbol("b")

    assert engine.parse_set(code) == "a = b + 5"
    assert engine.tokens == "".split()


def test_set_dot_notation() -> None:
    tokens = "set a to x dot b plus five".split()

    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("a")
    code.symbols.add_variable_symbol("x")

    assert engine.parse_set(code) == "a = x.b + 5"
    assert engine.tokens == "".split()
