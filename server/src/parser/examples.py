"""
Generates examples to be used for training our seq2seq model.
"""

import csv
import json
import logging
import os
import string
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Optional, TypeVar

T = TypeVar("T")
logger = logging.getLogger()


VERSIONED_DATA_DIR = Path("./data-versioned/examples")
UNVERSIONED_DATA_DIR = Path("./data-unversioned")

os.makedirs(UNVERSIONED_DATA_DIR, exist_ok=True)


def read_synonyms(filepath: Path) -> List[List[str]]:
    with open(filepath) as file:
        reader = csv.reader(file)

        return [list(row) for row in reader]


SYNONYMS = read_synonyms(VERSIONED_DATA_DIR / "synonyms.csv")
print(sum(map(len, SYNONYMS)))


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

    @staticmethod
    def parse(dct: Dict[str, str]) -> "Optional[Example]":
        try:
            return Example(dct["utterance"].strip(), dct["result"].split())
        except KeyError:
            return None

    def dump(self) -> Dict[str, str]:
        return {"utterance": self.utterance.strip(), "result": " ".join(self.result)}


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


def read_examples(filepath: Path) -> Iterator[Example]:
    with open(filepath) as file:
        examples = json.load(file)["examples"]

    for dct in examples:
        example = Example.parse(dct)
        if example:
            yield example


def read_templates(filepath: Path) -> List[Template]:
    with open(filepath) as file:
        contents = json.load(file)

    templates = (
        contents["templates"] + contents["sam-templates"] + contents["anmol-templates"]
    )

    return [Template.parse(template, result) for template, result in templates]


def make_examples(templates: List[Template]) -> Iterator[Example]:
    return flatten([template.generate(SYNONYMS) for template in templates])


def main() -> None:
    template_file = VERSIONED_DATA_DIR / "templates.json"
    examples_file = UNVERSIONED_DATA_DIR / "examples.json"

    templates = read_templates(template_file)

    examples = list(make_examples(templates))

    print(len(examples))

    example_json = {"examples": [e.dump() for e in examples]}

    with open(examples_file, "w") as file:
        json.dump(example_json, file, indent=2)


if __name__ == "__main__":
    main()

    # t = Template(
    #     "{append} result {to the end of} the product list",
    #     "append result to product list".split(),
    # )

    # for e in t.generate(SYNONYMS):
    #     print(e)
