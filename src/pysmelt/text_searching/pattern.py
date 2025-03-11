# Copyright (C) 2025 by Higher Expectations for Racine County

from functools import reduce
from itertools import pairwise
from re import compile, Match

from .element import Element
from .capture import Capture

class Pattern:
    r"""One regular expression with typed captures

    Parameters
    ----------
    elements: list[Element]
        the components, in order, of the regular expression.
    separator: str
        the pattern to delimit separate elements
    """
    def __init__(self, elements: list[Element], separator: str):
        self._elements = elements
        self._separator = separator
        self._names = [e.name for e in elements if e.is_named]
        self._re = compile(self.render())

    def __len__(self):
        return len(self._names)

    @property
    def names(self) -> list[str]:
        return self._names

    def quantified_separator(self, lhs: Element, rhs: Element) -> str:
        q = '*' if lhs.is_optional | rhs.is_optional else '+'
        return f"{self._separator}{q}"

    @staticmethod
    def separate(lhs: str, rhs: tuple[str, Element]) -> str:
        separator, e = rhs
        return f"{lhs}{separator}{e.render()}"

    def render(self) -> str:
        separators = [self.quantified_separator(*e)
                      for e in
                      pairwise(self._elements)]

        both = zip(separators, self._elements[1:])

        return reduce(self.separate, both, self._elements[0].render())

    def search(self, string: str) -> Match:
        return self._re.search(string)

    def captures(self, match: Match) -> list[Capture]:
        return [Capture(n, match[n]) for n in self._names] if bool(match) else []

    def extract(self, string: str) -> list[Capture]:
        return self.captures(self.search(string))

    @property
    def schema(self) -> list[tuple[str,str]]:
        return [(e.name, e.datatype) for e in self._elements if e.is_named]

    @staticmethod
    def from_json(parsed_json: dict) -> "Pattern":
        return Pattern([Element.from_json(e) for e in parsed_json["elements"]],
                       parsed_json.get("separator", r"\s"))
