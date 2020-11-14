import sys
from typing import Any, Dict, List, Optional

default_code_path = "./src/engine/default_code.py"


class Engine:
    def __init__(self):
        with open(default_code_path, "r") as fin:
            raw_code = fin.readlines()
            self.code = self.parse_code(self.stringify_code(raw_code))
        self.history = []
        self.history_pos = -1

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

    def set_code(self, raw_code):
        self.code = self.parse_code(raw_code)
        self.save_history()

    def get_code(self):
        return self.code

    def get_state(self) -> Dict[str, Any]:
        return {"code": self.code}

    def set_state(self, state: Dict[str, Any]):
        self.code = state["code"]

    def save_history(self):
        self.history = self.history[: self.history_pos + 1]
        self.history.append(self.get_state())
        self.history_pos = len(self.history) - 1

    def undo_history(self):
        if self.history_pos > 0:
            self.history_pos -= 1
        state = self.history[self.history_pos]
        self.set_state(state)
