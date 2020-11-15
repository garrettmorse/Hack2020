"""
Tries to test cycles of /operations/cycles
"""

from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.state_engine import StateEngine


def test_initial_utterance() -> None:
    rule_engine = RuleEngine()
    state_engine = StateEngine()

    tokens = "function read file one argument file location".split()

    rule_engine.add_tokens(tokens)
    new_code = rule_engine.parse(state_engine.code)
    state_engine.set_code(new_code)
    assert state_engine.print_code() == "def read_file(file_location):"
    assert rule_engine.tokens == []

    tokens = "if call len file location is less than twelve then".split()

    rule_engine.add_tokens(tokens)
    new_code = rule_engine.parse(state_engine.code)
    state_engine.set_code(new_code)
    assert (
        state_engine.print_code()
        == "def read_file(file_location):\n\tif len(file_location) < 12:"
    )
    assert rule_engine.tokens == []
