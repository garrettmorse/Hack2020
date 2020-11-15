from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_delete_end() -> None:
    tokens = "function y two argument x and y".split()
    rule_engine = RuleEngine(tokens)

    code = Code()

    for i in range(10):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)

    tokens = "delete line end".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert len(code.lines) == 10
    assert "8" in code.lines[-1]

def test_delete_beginning() -> None:
    tokens = "function y two argument x and y".split()
    rule_engine = RuleEngine(tokens)

    code = Code()

    for i in range(10):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)

    tokens = "delete line end".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert len(code.lines) == 10
    assert "def" not in code.lines[0]

def test_delete_line() -> None:
    tokens = "function y two argument x and y".split()
    rule_engine = RuleEngine(tokens)

    code = Code()

    for i in range(10):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)

    tokens = "delete line three".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert len(code.lines) == 10
    assert "2" in code.lines[2]
