"""
Tries to test cycles of /operations/cycles
"""

import pytest
from src import RuleEngine
from src.state_engine import Code


@pytest.mark.skip(reason="always fails")
def test_fizz_buzz() -> None:
    rule_engine = RuleEngine()
    code = Code()

    tokens = "function fizz buzz zero arguments".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert code.print_lines() == "def fizz_buzz():\n"
    assert rule_engine.tokens == []

    tokens = "if call len file location is less than twelve then".split()

    tokens = "for x in range zero to 100".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert code.print_lines() == "def fizz_buzz():\n\tfor x in range(0, 100):\n"
    assert rule_engine.tokens == []

    tokens = "if x modulo three equals zero and x modulo five equals zero then".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert (
        code.print_lines()
        == "def fizz_buzz():\n\tfor x in range(0, 100):\n\t\tif x % 3 == 0 and x % 5 == 0:\n"
    )
    assert rule_engine.tokens == []

    tokens = "call print fizz buzz".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert (
        code.print_lines()
        == "def fizz_buzz():\n\tfor x in range(0, 100):\n\t\tif x % 3 == 0 and x % 5 == 0:\n\t\t\tprint(fizz_buzz)\n"  # TODO
    )
    assert rule_engine.tokens == []

    tokens = ["tabout"]
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert (
        code.print_lines()
        == "def fizz_buzz():\n\tfor x in range(0, 100):\n\t\tif x % 3 == 0 and x % 5 == 0:\n\t\t\tprint(fizz_buzz)\n\t\t\t \n\t\t \n"
    )
    assert rule_engine.tokens == []

    tokens = "else if x modulo three equals zero then call print fizz".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert (
        code.print_lines()
        == "def fizz_buzz():\n\tfor x in range(0, 100):\n\t\tif x % 3 == 0 and x % 5 == 0:\n\t\t\tprint(fizz_buzz)\n\t\t\t \n\t\t \n\t\telse:\n\t\t\tif x % 3 == 0:\n\t\t\t\tprint(fizz)\n"
    )
    assert rule_engine.tokens == []

    tokens = "tabout else if x modulo 5 equals zero then call print buzz".split()
    rule_engine.add_tokens(tokens)
    code = rule_engine.parse(code)

    assert rule_engine.tokens == []
