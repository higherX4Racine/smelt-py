#  Copyright (c) 2025 by Higher Expectations for Racine County


from typing import Any
from .pattern import Pattern
from .type_map import TypeMap


class Parser:
    def __init__(self, mapping: TypeMap, pattern: Pattern):
        if not mapping.keys.issuperset(pattern.names):
            raise ValueError("The mapping's keys must include all of the pattern's names.")
        self._mapping = mapping
        self._pattern = pattern

    def __call__(self, text: str) -> dict[str, Any] | None:
        captures = self._pattern.extract(text)
        if captures:
            return self._mapping.typed_captures(captures)
        return None