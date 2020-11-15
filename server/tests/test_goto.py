from src import rule_engine
from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_goto_end() -> None:
    tokens = "function y two argument x and y"
    engine = RuleEngine(tokens)

    code = Code()

    for i in range(10):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)
        code = rule_engine.parse(code)

    tokens = "goto line end".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert len(code.lines) == 11
    assert code.cursor_position ==

def test_delete_beginning() -> None:
    tokens = "function y two argument x and y"
    engine = RuleEngine(tokens)

    code = Code()

    for i in range(10):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)
        code = rule_engine.parse(code)

    tokens = "delete line end".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert len(code.lines) == 10
    assert "def" not in code.lines[0]

def test_delete_line() -> None:
    tokens = "function y two argument x and y"
    engine = RuleEngine(tokens)

    code = Code()

    for i in range(10):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)
        code = rule_engine.parse(code)

    tokens = "delete line three".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert len(code.lines) == 10
    assert "2" in code.lines[2]
