#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any, Type

from polars import (
    Binary,
    col,
    DataFrame,
    Object,
    Schema,
    String,
)

from .utilities import as_filter_expressions


class ModelFramer[T]:
    r"""base class that wraps a polars DataFrame with some other behavior."""

    def __init__(self, builder: Type[T], schema: Schema | dict):
        self._builder = builder
        self._frame = DataFrame(schema=schema)

    @property
    def frame(self) -> DataFrame:
        return self._frame

    def __getitem__(self, item: int) -> T:
        return self.as_instance(**self.frame.row(index=item, named=True))

    def as_instance(self, **kwargs: dict[str,Any]) -> T:
        return self._builder(**kwargs)

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
        instance = self.as_instance(**typed_captures)
        if row_frame.height == 0:
            row_frame = self.as_row(instance)
            self._frame.vstack(row_frame, in_place=True)
        return instance
