# Copyright 2025 by Higher Expectation for Racine County

from typing import Any

from polars import (
    datatypes,
    Schema,
    String,
)

from polars.datatypes import DataType

from .capture import Capture, TypedCapture
from .pattern import Pattern


class PolarsCaster:

    def __init__(self, schema: Schema):
        self._type_map = schema.to_python()

    @staticmethod
    def polars_type(type_name: str, default_type: DataType = None) -> DataType:
        default_type = default_type or String
        return getattr(datatypes, type_name, default_type)

    @classmethod
    def to_polars_schema(cls, pattern: Pattern, default_type: DataType = None) -> Schema:
        return Schema({k: cls.polars_type(v, default_type) for k, v in pattern.schema})

    def cast(self, capture: Capture) -> Any:
        return self._type_map[capture.name](capture.value)

    def cast_captures(self, captures: list[Capture]) -> list[TypedCapture]:
        return [TypedCapture(c.name, self.cast(c)) for c in captures]
