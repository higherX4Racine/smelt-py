from typing import Any
from .output_rule import OutputRule


class Passthrough(OutputRule):
    def __init__(self, index: int):
        super().__init__("passthrough")
        self._index = index

    def __call__(self, row: tuple) -> Any:
        return row[self._index]
