#  Copyright (c) 2025 by Higher Expectations for Racine County


from polars import Binary

from .model_framer import ModelFramer, Schema, Type
from ..models import Context


class ContextFramer(ModelFramer):
    def __init__(self,
                 context_type: Type[Context],
                 schema: Schema | dict[str, ...]):
        super().__init__(context_type,
                         {"context_id": Binary} | schema)
