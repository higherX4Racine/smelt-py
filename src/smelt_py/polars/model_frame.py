#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any, ClassVar
from polars import DataFrame, Schema, col, Binary, Object, String
from .utilities import as_filter_expressions


class ModelFrame[T]:
    r"""base class that wraps a polars DataFrame with some other behavior."""

    ModelClass: ClassVar[type] = T

    def __init__(self, prototype: T):
        self._frame = DataFrame(schema=prototype.schema())

    @property
    def frame(self) -> DataFrame:
        return self._frame

    def as_row(self, model_item: T) -> DataFrame:
        return DataFrame([model_item.as_tuple()],
                         schema=self._frame.schema,
                         orient="row")

    def sanitize_blobs(self) -> DataFrame:
        return self._frame.with_columns(
            col(Object).map_elements(repr, return_dtype=String),
            col(Binary).bin.encode("hex")
        )

    def find_or_append(self,
                       typed_captures: dict[str, Any],
                       fields: list[str] = None) -> T:
        expr = as_filter_expressions(typed_captures, fields)
        row_frame = self._frame.filter(*expr)
        if row_frame.height > 0:
            typed_captures = row_frame.row(0, named=True)
        context = self.ModelClass(**typed_captures)
        if row_frame.height == 0:
            row_frame = self.as_row(context)
            self._frame.vstack(row_frame, in_place=True)
        return context
