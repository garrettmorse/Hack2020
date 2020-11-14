from typing import Any, Dict, List

from .code import Code
from .line import Line

default_code_path = "./src/state_engine/default_code.py"


class StateEngine:
    def __init__(self):
        with open(default_code_path, "r") as fin:
            raw_code = "".join(fin.readlines())
            self.code: Code = Code.from_raw(raw_code)
        self.history: List[Code] = []
        self.history_pos: int = -1

    def set_code(self, raw_code: str):
        self.code = Code.from_raw(raw_code)
        self.save_history()

    def print_code(self):
        return self.code.print_lines()

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