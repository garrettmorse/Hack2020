"""
Generates examples to be used for training our seq2seq model.
"""

import csv
import itertools
import json
import logging
import os
import random
import re
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, TypeVar

from . import disk

T = TypeVar("T")


logger = logging.getLogger()


random.seed(42)


def read_synonyms(filepath: Path) -> List[List[str]]:
    with open(filepath) as file:
        reader = csv.reader(file)

        return [list(row) for row in reader]


SYNONYMS = read_synonyms(disk.VERSIONED_DATA_DIR / "synonyms.csv")
print(sum(map(len, SYNONYMS)), "synonyms")

VARIABLES = read_synonyms(disk.VERSIONED_DATA_DIR / "variables.csv")
print(sum(map(len, VARIABLES)), "variables")

int_pattern = re.compile("\$int\d+")
string_pattern = re.compile("\$string\d+")
list_pattern = re.compile("\$list\d+")
bool_pattern = re.compile("\$bool\d+")
path_pattern = re.compile("\$path\d+")


PATTERNS = [int_pattern, string_pattern, list_pattern, bool_pattern, path_pattern]

# UTIL


def flatten(lst: Iterable[Iterable[T]]) -> Iterator[T]:
    for sublist in lst:
        for item in sublist:
            yield item


def get(s: Iterable[T]) -> T:
    return next(iter(s))


@dataclass
class Example:
    utterance: str
    result: List[str]

    def dump(self) -> Dict[str, str]:
        return {"utterance": self.utterance.strip(), "code": " ".join(self.result)}

    def expand(self) -> "Iterator[Example]":
        """
        Expands all $bool, $int, etc with possible values from variables.csv
        """

        if "$" not in self.utterance:
            yield self
            return

        for pattern, variables in zip(PATTERNS, VARIABLES):
            matches = re.findall(pattern, self.utterance)
            if not matches:
                continue

            for match in matches:
                for var in variables[1:]:  # skip first one
                    for e in Example(
                        self.utterance.replace(match, var),
                        " ".join(self.result).replace(match, var).split(),
                    ).expand():
                        yield e

    def __hash__(self):
        return hash(repr(self))


@dataclass
class Template:
    """
    A template is a named format string with the arg names being words. Each arg can be replaced with any synonym and produce the same meaning.
    """

    template: str
    result: List[str]

    @staticmethod
    def parse(template: str, result: str) -> "Template":
        return Template(template, result.split())

    def generate(self, synonyms: List[List[str]]) -> List[Example]:
        fields = set()
        for _, field, _, _ in string.Formatter().parse(self.template):
            if field is None:
                continue
            fields.add(field)

        default_args = {field: field for field in fields}

        results = []

        # create a new args object where each field loops through all of its synonyms
        for args in self._generate_args(default_args, synonyms):
            results.append(Example(self.template.format(**args), self.result))

        return results

    def _generate_args(
        self, default_args: Dict[str, str], synonyms: List[List[str]]
    ) -> Iterator[Dict[str, str]]:
        """
        Recursively generate all possible combinations.

        Calls _generate_args with default_args having one fewer term in it n times, where n is the number of synonyms the first element in default_args has
        """

        if not default_args:
            yield {}
            return

        first_arg = get(default_args.keys())

        other_args = {key: val for key, val in default_args.items() if key != first_arg}

        for word_synonyms in synonyms:
            if word_synonyms[0] == first_arg:  # only compare first synonym as "truth"
                break
            elif first_arg in word_synonyms:
                logger.warning(
                    f"'{first_arg}' in word synonyms ({word_synonyms}) but not first element."
                )
        else:
            logger.warning(f"'{first_arg}' marked as synonym but has no synonyms.")
            word_synonyms = [first_arg]

        assert word_synonyms[0] == first_arg

        for synonym in word_synonyms:
            for other_generated_args in self._generate_args(other_args, synonyms):
                yield {**other_generated_args, first_arg: synonym}


def read_templates(filepath: Path) -> List[Template]:
    with open(filepath) as file:
        contents = json.load(file)

    templates = (
        contents["templates"]
        + contents["sam-templates"]
        + contents["anmol-templates"]
        + contents["jason-templates"]
        + contents["missed-templates"]
    )

    return [Template.parse(template, result) for template, result in templates]


def make_examples(templates: List[Template]) -> Iterator[Example]:
    unexpanded = flatten([template.generate(SYNONYMS) for template in templates])

    expanded = [e.expand() for e in unexpanded]

    return itertools.chain(*expanded)


def main() -> None:
    template_file = disk.VERSIONED_DATA_DIR / "templates.json"

    templates = read_templates(template_file)

    examples = make_examples(templates)

    os.makedirs(disk.VERSIONED_DATA_DIR / "generated", exist_ok=True)

    with open(disk.VERSIONED_DATA_DIR / "generated" / "examples.json", "w") as file:
        for i, ex in enumerate(examples):
            file.write(json.dumps(ex.dump()) + "\n")

    print(f"Synthesized {i} examples.")


if __name__ == "__main__":
    main()

    # t = Template(
    #     "$int1 equals $int2",
    #     "set $int1 to $int2".split(),
    # )

    # ex = t.generate(SYNONYMS)[0]
    # for e in ex.expand():
    #     print(e)
