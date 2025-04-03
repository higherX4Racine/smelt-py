#  Copyright (C) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass, field, InitVar
from typing import Any
from ..keys import CompositeKey
from .base import Base


@dataclass
class Column(Base):
    source_id: InitVar[bytes] = field(init=False)
    index: InitVar[int] = field(init=False)
    context_type: str
    context_id: bytes
    measure_type: type

    def __post_init__(self, source_id: bytes, index: int):
        self._column_key = CompositeKey(source_id, index)

    @classmethod
    def field_names(cls) -> list[str]:
        return [
            "source_id",
            "index",
            "context_type",
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
