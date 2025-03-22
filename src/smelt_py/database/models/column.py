#  Copyright (C) 2025 by Higher Expectations for Racine County

from typing import Any
from ..keys import CompositeKey
from .base import Base


class Column(Base):
    r"""One observed column from a Panorama data source

    Parameters
    ----------
    source_id: int
        A foreign key to a table of `Source` objects
    index: int
        Which column in the source, starting from zero, it came from
    context_type: type
        The subclass of `Context` that holds data from this column's heading
    measure_type: type
        The datatype of the items in this column's cells.

    See Also
    --------
    CompositeKey
    Context
    Source
    """

    def __init__(self,
                 source_id: bytes,
                 index: int,
                 context_type: str,
                 context_id: bytes,
                 measure_type: Any):
        self._column_key = CompositeKey(source_id, index)
        self._context_type = context_type
        self._context_id = context_id
        self._measure_type = measure_type

    @classmethod
    def field_names(cls) -> list[str]:
        return super(cls).field_names() + [
            "source_id",
            "index",
            "context_type"
            "context_id",
            "measure_type"
        ]

    @property
    def column_id(self) -> bytes:
        r"""The primary key for this item, concatenating `source_id` and `index`"""
        return self._column_key.key

    @property
    def source_id(self) -> bytes:
        return self._column_key.unique_id

    @property
    def index(self) -> int:
        return self._column_key.index

    @property
    def context_type(self) -> str:
        return self._context_type

    @property
    def context_id(self) -> bytes:
        return self._context_id

    @property
    def measure_type(self) -> Any:
        return self._measure_type
