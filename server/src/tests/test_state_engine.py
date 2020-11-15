from src import RuleEngine, StateEngine


def test_multiple_commands() -> None:
    state_engine = StateEngine()
    rule_engine = RuleEngine()

    tokens = ["function", "main", "zero", "argument"]
    rule_engine.add_tokens(tokens)
    assert rule_engine.tokens == tokens

    code_copy = state_engine.get_code_deepcopy()
    prev_num_lines = len(code_copy.lines)
    new_code = rule_engine.parse(code_copy)
    assert len(new_code.lines) == prev_num_lines + 1
    new_code_lines = new_code.print_lines()

    assert (
        new_code_lines
        == "import os\nimport sys\n\n# Start talking to get started!\n#\n# If nothing comes to mind, here's a good example to get started...\n#	define a function main that takes no arguments\n#	print helloworld\n#	call main\n\ndef main():"
    )

    state_engine.set_code(new_code)
    tokens = ["call", "print", "twelve"]
    rule_engine.add_tokens(tokens)
    assert rule_engine.tokens == tokens

    code_copy = state_engine.get_code_deepcopy()

    prev_num_lines = len(code_copy.lines)
    new_code = rule_engine.parse(code_copy)
    assert len(new_code.lines) == prev_num_lines + 1

    new_code_lines = new_code.print_lines()

    assert (
        new_code_lines
        == "import os\nimport sys\n\n# Start talking to get started!\n#\n# If nothing comes to mind, here's a good example to get started...\n#	define a function main that takes no arguments\n#	print helloworld\n#	call main\n\ndef main():\n\tprint(12)"
    )

    state_engine.set_code(new_code)
