from __future__ import annotations

import copy
from typing import Any, Dict, List, Union

from .code import Code, Line

StateInternal = Union[Code]
State = Dict[str, StateInternal]
default_code_path = "./src/state_engine/default_code.py"


class StateEngine:
    def __init__(self):
        with open(default_code_path, "r") as fin:
            raw_code = "".join(fin.readlines())
            self.code: Code = Code.from_raw(raw_code)
        self.history: List[State] = []
        self.history_pos: int = -1

    def set_code(self, raw_code: str) -> None:
        self.code = Code.from_raw(raw_code)
        self.save_history()

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

    def deepcopy(self) -> StateEngine:
        return copy.deepcopy(self)
