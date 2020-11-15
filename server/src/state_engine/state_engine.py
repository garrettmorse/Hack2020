from __future__ import annotations

import copy
from typing import Dict, List, Union

from .code import Code

default_code_path = "./src/state_engine/default_code.py"


class StateEngine:
    def __init__(self) -> None:
        with open(default_code_path, "r") as fin:
            raw_code = "".join(fin.readlines())
            self.code = Code.from_raw(raw_code)
        self.history: List[Code] = []

    def parse_and_set_code(self, raw_code: str) -> None:
        self.code = Code.from_raw(raw_code)
        self.save_history()

    def set_code(self, code: Code) -> None:
        self.code = code
        self.save_history()

    def get_code_deepcopy(self) -> Code:
        return copy.deepcopy(self.code)

    def print_code(self) -> str:
        return self.code.print_lines()

    def save_history(self) -> None:
        self.history.append(self.code)

    def undo_history(self) -> None:
        self.code = self.history.pop()
