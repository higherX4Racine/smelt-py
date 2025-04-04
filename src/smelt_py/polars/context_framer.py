#  Copyright (c) 2025 by Higher Expectations for Racine County
from polars import Binary

from .model_framer import ModelFramer, Schema, Type


class ContextFramer[T](ModelFramer):
    def __init__(self, builder: Type[T], schema: Schema | dict[str,...]):
        super().__init__(builder,
                         {"context_id": Binary} | schema)
