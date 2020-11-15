from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_goto_end() -> None:
    tokens = "function y two argument x and y".split()
    rule_engine = RuleEngine(tokens)

    code = Code([])

    for i in range(10):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)

    tokens = "goto line end".split()
    rule_engine.add_tokens(tokens)

    print(code.print_lines())
    new_code = rule_engine.parse(code)
    print(new_code.print_lines())

    print(rule_engine.tokens)
    assert len(new_code.lines) == 11
    assert new_code.cursor_position == 11


def test_goto_beginning() -> None:
    tokens = "function y two argument x and y".split()
    rule_engine = RuleEngine(tokens)

    code = Code([])

    for i in range(10, 20):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)

    tokens = "goto line beginning".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert len(code.lines) == 11
    assert code.cursor_position == 1

def test_goto_three() -> None:
    tokens = "function y two argument x and y".split()
    rule_engine = RuleEngine(tokens)

    code = Code([])

    for i in range(20, 30):
        tokens = f"set x to {i}".split()

        rule_engine.add_tokens(tokens)

    tokens = "goto line three".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)
    print(code.print_lines())
    assert len(code.lines) == 11
    assert code.cursor_position == 3
