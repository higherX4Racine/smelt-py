#  Copyright (c) 2025 by Higher Expectations for Racine County

from polars import (
    Binary,
    Int64,
    Object,
    Schema,
    String,
)

from ..models import Column, Context
from .model_framer import ModelFramer


class ColumnFramer(ModelFramer):
    def __init__(self):
        super().__init__(Column,
                         Schema({
                             'source_id': Binary,
                             'index': Int64,
                             'context_label': String,
                             'context_id': Binary,
                             'measure_type': Object
                         }))

    def add_column(self,
                   source_context: Context,
                   index: int,
                   heading_key: str,
                   heading_context: Context) -> Column:
        _column = Column(source_context.context_id, index,
                         heading_key, heading_context.context_id,
                         heading_context.output_type)
        self._frame.vstack(self.as_row(_column), in_place=True)
        return _column
