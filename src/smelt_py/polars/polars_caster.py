#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any

from polars import (
    datatypes,
    Schema,
    String,
)

from polars.datatypes import DataType

from ..capture import Capture


class PolarsCaster:

    def __init__(self, schema: Schema):
        self._type_map = schema.to_python()

    @staticmethod
    def polars_type(type_name: str, default_type: DataType = None) -> DataType:
        default_type = default_type or String
        return getattr(datatypes, type_name, default_type)

    def cast(self, capture: Capture) -> Any:
        return self._type_map[capture.name](capture.value)

    def cast_captures(self, captures: list[Capture]) -> list[Capture]:
        return [Capture(c.name, self.cast(c)) for c in captures]
