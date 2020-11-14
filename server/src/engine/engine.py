import sys
from typing import List

default_code = "./src/engine/default_code.py"


class Engine:
    def __init__(self):
        with open(default_code, "r") as fin:
            self.code: List[str] = fin.readlines()

    def stringify_and_get_code(self) -> str:
        return "".join(self.code)

    def parse_and_set_code(self, code: str) -> None:
        lines = code.split("\n")
        code = [line + "\n" for line in lines]
        self.code = code
