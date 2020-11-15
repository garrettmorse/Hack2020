from __future__ import annotations

from typing import List, Optional, Type

from .symbols import Symbols


class Line:
    def __init__(self, value: str, line_number: int, tab_number: int) -> None:
        self.value = value
        self.line_number = line_number
        self.tab_number = tab_number


class Code:
    def __init__(self, lines: List[Line] = [], global_tab_number: int = 0) -> None:
        self.lines = lines
        self.global_tab_number = global_tab_number
        self.print_lines_cache: Optional[str] = None
        self.symbols = Symbols()
        self.symbols.add_function_symbol("print", "arg")
        self.symbols.add_function_symbol("len", "arg")

    def add_line(self, value: str, tab_out_number: int = 0) -> None:
        self.print_lines_cache = None
        self.lines.append(Line(value, len(self.lines) + 1, self.global_tab_number))

        if value[-1] == ":":
            self.global_tab_number += 1
        if tab_out_number != 0:
            self.global_tab_number -= tab_out_number

    def print_lines(self) -> str:
        if not self.print_lines_cache:
            results = [
                ((line.tab_number * "\t") + line.value + "\n") for line in self.lines
            ]
            self.print_lines_cache = "".join(results).rstrip()
        return self.print_lines_cache

    @classmethod
    def from_raw(self: Type[Code], raw_code: str) -> Code:
        replace_dict = {"    ": "\t", "\r\n": "\n"}
        for k, v in replace_dict.items():
            raw_code = raw_code.replace(k, v)
        raw_lines = raw_code.split("\n")

        lines = []

        for index, raw_line in enumerate(raw_lines):
            pos = 0
            while raw_line and pos < len(raw_line) and raw_line[pos] == "\t":
                pos += 1
            lines.append(Line(raw_line[pos:], index, pos))

        last_line = lines[-1]
        global_tab_number = last_line.tab_number
        if last_line.value and last_line.value[-1] == ":":
            global_tab_number += 1

        return self(lines, global_tab_number)
