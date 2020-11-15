from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_no_defined_func_call() -> None:
    tokens = "return a plus b".split()

    engine = RuleEngine(tokens)

    code = Code()
    code.symbols.add_variable_symbol("a")
    code.symbols.add_variable_symbol("b")

    assert engine.parse_return(code) == "return a + b"
    assert engine.tokens == "".split()
