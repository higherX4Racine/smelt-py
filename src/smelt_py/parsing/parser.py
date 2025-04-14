#  Copyright (c) 2025 by Higher Expectations for Racine County
from collections.abc import Iterable

from typing import Any
from .pattern import Pattern, Element, Capture
from .converters import Converter


class Parser:
    def __init__(self,
                 elements: Iterable[Element],
                 separator: str,
                 **kwargs: Converter):
        pattern = Pattern(elements, separator)
        if not set(kwargs.keys()).issuperset(pattern.names):
            raise ValueError("The mapping's keys must include all of the pattern's names.")
        self._mapping = kwargs
        self._pattern = pattern

    def parse(self, text: str) -> dict[str, Any] | None:
        captures = self._pattern.extract(text)
        if captures:
            return self.convert_captures(captures)
        return None

    def convert(self, item: Capture | str, text: str = None) -> Any:
        if isinstance(item, Capture):
            return self._mapping[item.name](item.value)
        return self._mapping[item](text)

    def convert_captures(self, captures: list[Capture]) -> dict[str, Any]:
        return {
            name: self.convert(name, value) for
            name, value in
            captures
        }
