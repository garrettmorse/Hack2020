from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_basic_call() -> None:
    tokens = "x".split()

    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_function(code) == "f(a, b)"
    assert engine.tokens == "".split()
