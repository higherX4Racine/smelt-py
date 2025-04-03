#  Copyright (c) 2025 by Higher Expectations for Racine County
from typing import Any, Callable
from polars import Schema

from ..models import Context as ContextModel
from .model_frame import Frame
from .utilities import as_row, as_filter_expressions


class Context(Frame):
    r"""Composed of a Context subclass and """

    def __init__(self, context_class: Callable, schema: dict | Schema):
        super().__init__(schema)
        self._context_class = context_class

    def find_or_append(self,
                       typed_captures: dict[str, Any],
                       fields: list[str] = None) -> ContextModel:
        expr = as_filter_expressions(typed_captures, fields)
        row_frame = self._frame.filter(*expr)
        if row_frame.height > 0:
            typed_captures = row_frame.row(0, named=True)
        context = self._context_class(**typed_captures)
        if row_frame.height == 0:
            row_frame = as_row(context, self._frame)
            self._frame.vstack(row_frame, in_place=True)
        return context
