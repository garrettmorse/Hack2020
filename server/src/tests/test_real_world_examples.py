from src import BartEngine, RuleEngine
from src.state_engine import Code

bart = BartEngine()
rule = RuleEngine()


def test1() -> None:
    code = Code()
    code.add_line("x = 5")
    code.add_line("print(x)")
    code.symbols.add_variable_symbol("x")

    print(code.symbols.variable_symbols)

    raw_text = "set x equal to x + 4 "

    tokens = bart.predict(raw_text)

    rule.add_tokens(tokens)
    code = rule.parse(code)
    print(code.print_lines())


if __name__ == "__main__":
    test1()
