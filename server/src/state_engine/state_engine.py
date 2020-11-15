from __future__ import annotations

import copy
from typing import Dict, List, Union

from .code import Code

StateInternal = Union[Code]
State = Dict[str, StateInternal]
default_code_path = "./src/state_engine/default_code.py"


class StateEngine:
    def __init__(self) -> None:
        with open(default_code_path, "r") as fin:
            raw_code = "".join(fin.readlines())
            self.code = Code.from_raw(raw_code)
        self.history: List[State] = []
        self.history_pos = -1

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

    def get_state(self) -> State:
        return {"code": self.code}

    def set_state(self, state: State) -> None:
        self.code = state["code"]

    def save_history(self) -> None:
        self.history = self.history[: self.history_pos + 1]
        self.history.append(self.get_state())
        self.history_pos = len(self.history) - 1

    def undo_history(self) -> None:
        if self.history_pos > 0:
            self.history_pos -= 1
        state = self.history[self.history_pos]
        self.set_state(state)
