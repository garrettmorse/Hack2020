class Line:
    def __init__(self, value: str, line_number: int, tab_number: int):
        self.value = value
        self.line_number = line_number
        self.tab_number = tab_number


class Code:
    def __init__(self):
        self.lines = []
        self.global_tab_number = 0

    def add_line(self, value: str, tab_out_number: int = 0):
        self.lines.append(Line(value, len(self.lines) + 1, self.global_tab_number))

        if value[-1] == ":":
            self.global_tab_number += 1
        if tab_out_number != 0:
            self.global_tab_number -= tab_out_number

    def print_lines(self):
        results = [
            ((line.tab_number * "\t") + line.value + "\n") for line in self.lines
        ]
        return "".join(results)

    def from_lines(self, raw_code: str):
        replace_dict = {"    ": "\t", "\r\n": "\n"}
        for k, v in replace_dict.items():
            raw_code = raw_code.replace(k, v)
        raw_lines = raw_code.split("\n")

        lines = []

        for index, raw_line in enumerate(raw_lines):
            pos = 0
            while raw_line[pos] == "\t":
                pos += 1
            lines.append(Line(raw_line[pos:], index, pos))

        self.lines = lines
        last_line = self.lines[-1]
        self.global_tab_number = last_line.tab_number + (
            1 if last_line.value[-1] == ":" else 0
        )
