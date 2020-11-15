from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_if_basic() -> None:
    tokens = "if x less than y then".split()

    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("x")
    code.symbols.add_variable_symbol("y")

    assert engine.parse_if(code) == "if x < y:"
    assert engine.tokens == []


def test_if_with_statement() -> None:
    tokens = "if x less than three then set x to three".split()

    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("x")

    assert engine.parse_if(code) == "if x < 3:"
    assert engine.tokens == "set x to three".split()


def test_if_with_else() -> None:
    tokens = "if x greater than or equal to three then set x to three else set x to zero".split()

    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("x")

    assert engine.parse_if(code) == "if x >= 3:"
    assert engine.tokens == "set x to three else set x to zero".split()
