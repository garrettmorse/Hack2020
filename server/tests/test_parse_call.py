from src.rule_engine.rule_engine import RuleEngine
from src.state_engine.code import Code


def test_no_defined_func_call() -> None:
    tokens = "call f a b".split()

    engine = RuleEngine(tokens)

    code = Code()

    assert engine.parse_call(code) == "f(a, b)"
    assert engine.tokens == "".split()


def test_basic_call() -> None:
    func_tokens = "function f two arguments a and b return a plus b".split()

    engine = RuleEngine(func_tokens)

    code = Code()
    code = engine.parse(code)
    code.symbols.add_variable_symbol("a")
    code.symbols.add_variable_symbol("b")
    tokens = "call f a b".split()
    engine.add_tokens(tokens)

    assert engine.parse_call(code) == "f(a, b)"
    assert engine.tokens == "".split()


def test_basic_call_with_digits() -> None:
    func_tokens = "function f two arguments a and b return a plus b".split()

    engine = RuleEngine(func_tokens)

    code = Code()
    code = engine.parse(code)
    code.symbols.add_variable_symbol("a")
    code.symbols.add_variable_symbol("b")
    tokens = "call f two four".split()
    engine.add_tokens(tokens)

    assert engine.parse_call(code) == "f(2, 4)"
    assert engine.tokens == "".split()


def test_hard_call() -> None:
    func_tokens = "function f one argument file name return one".split()

    engine = RuleEngine(func_tokens)

    code = Code()
    code = engine.parse(code)
    tokens = "call f file path".split()
    engine.add_tokens(tokens)

    assert engine.parse_call(code) == "f(file_path)"
    assert engine.tokens == "".split()


def test_call_with_multi_words() -> None:
    func_tokens = "function read file one argument file name return one".split()

    engine = RuleEngine(func_tokens)

    code = Code()
    code = engine.parse(code)

    tokens = "call read file path".split()
    engine.add_tokens(tokens)

    assert engine.parse_call(code) == "read_file(path)"
    assert engine.tokens == "".split()


def test_call_with_multi_words4() -> None:
    func_tokens = "function read file one argument file name return one".split()

    engine = RuleEngine(func_tokens)

    code = Code()
    code = engine.parse(code)

    tokens = "call read file file path".split()
    engine.add_tokens(tokens)

    assert engine.parse_call(code) == "read_file(file_path)"
    assert engine.tokens == "".split()


def test_call_with_multi_words3() -> None:
    func_tokens = (
        "function read file two arguments file name and length return length".split()
    )

    engine = RuleEngine(func_tokens)

    code = Code()
    code = engine.parse(code)
    code.symbols.add_variable_symbol("file_path")

    tokens = "call read file file path twelve".split()
    engine.add_tokens(tokens)

    assert engine.parse_call(code) == "read_file(file_path, 12)"
    assert engine.tokens == "".split()


def test_call_with_multi_words2() -> None:
    func_tokens = (
        "function read file two arguments file name and length return length".split()
    )

    engine = RuleEngine(func_tokens)

    code = Code()
    code = engine.parse(code)
    code.symbols.add_variable_symbol("file_path")

    tokens = "call read file foo dot txt twelve".split()
    engine.add_tokens(tokens)

    assert engine.parse_call(code) == "read_file('foo.txt', 12)"
    assert engine.tokens == "".split()
