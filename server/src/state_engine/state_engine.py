from typing import Any, Dict, List

default_code_path = "./src/state_engine/default_code.py"


class StateEngine:
    def __init__(self):
        with open(default_code_path, "r") as fin:
            raw_code = fin.readlines()
            self.code = self.parse_code(self.stringify_code(raw_code))
        self.history = []
        self.history_pos = -1

    @classmethod
    def stringify_code(self, code: List[str]) -> str:
        return "".join(code)

    @classmethod
    def parse_code(self, raw_code: str) -> List[str]:
        replace_dict = {"    ": "\t", "\r\n": "\n"}
        for k, v in replace_dict.items():
            raw_code = raw_code.replace(k, v)
        lines = raw_code.split("\n")
        code = [line + "\n" for line in lines]
        return code

    def set_code(self, raw_code: str):
        self.code = StateEngine.parse_code(raw_code)
        self.save_history()

    def get_code(self):
        return StateEngine.stringify_code(self.code)

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
