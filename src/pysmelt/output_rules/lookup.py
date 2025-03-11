from typing import Any

from .output_rule import OutputRule


class Lookup(OutputRule):
    def __init__(self, index: int, mapping: dict[str, str]):
        super().__init__("lookup")
        self._index = index
        self._mapping = mapping

    def __call__(self, row: tuple) -> Any:
        return self._mapping[row[self._index]]
