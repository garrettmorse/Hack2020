import sys
from typing import List

default_code = "./src/engine/default_code.py"


class Engine:

    def __init__(self):
        with open(default_code, "r") as fin:
            self.code: List[str] = fin.readlines()
            self.history = []
            self.history_pointer = -1

    def stringify_and_get_code(self) -> str:
        return "".join(self.code)

    def parse_and_set_code(self, code: str) -> None:
        lines = code.split("\n")
        code = [line + "\n" for line in lines]
        self.code = code

    def _save_history(self, code):
        self.history = self.history[:history_pointer + 1]
        self.history.append(code)
        self.history_pointer = len(self.history) - 1

    def _undo(self, code):
        if self.history_pointer > 0:
            self.history_pointer -= 1
        return self.history[self.history_pointer]
