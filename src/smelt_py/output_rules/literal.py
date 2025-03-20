from typing import Any

from .output_rule import OutputRule


class Literal(OutputRule):
    def __init__(self, value: str):
        super().__init__("literal")
        self._value = value

    def __call__(self, row: tuple) -> Any:
        return self._value
