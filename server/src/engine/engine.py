import sys
from typing import List, Optional

default_code_path = "./src/engine/default_code.py"


class Engine:
    def __init__(self):
        with open(default_code_path, "r") as fin:
            raw_code = fin.readlines()
            self.code: List[str] = self.parse_code(self.stringify_code(raw_code))

        self.history = []
        self.history_position: int = -1

    def stringify_code(self, raw: Optional[str] = None) -> str:
        raw = raw if raw else self.code
        return "".join(raw)

    def parse_code(self, raw: Optional[str]) -> str:
        raw = raw if raw else self.code
        replace_dict = {"    ": "\t", "\r\n": "\n"}
        for k, v in replace_dict.items():
            raw = raw.replace(k, v)
        lines = raw.split("\n")
        code = [line + "\n" for line in lines]
        return code

    def save_history(self):
        data = {"code": self.code}

        self.history = self.history[: self.history_position + 1]
        self.history.append(data)
        self.history_position = len(self.history) - 1

    def undo(self, code):
        if self.history_position > 0:
            self.history_position -= 1
        return self.history[self.history_position]

    def redo(self):
        pass
