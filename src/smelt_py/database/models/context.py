#  Copyright (C) 2025 by Higher Expectations for Racine County

from typing import Any
from ..keys import UniqueKey
from .base import Base


class Context(Base):
    r"""Data extracted from the heading of a column.

    Parameters
    ----------
    context_id: bytes
        The primary key of this item, optional. Defaults to `uuid.uuid4()`
    """

    def __init__(self, context_id: bytes = None):
        self._context_id = context_id if \
            context_id is not None else \
            UniqueKey.new().key

    @classmethod
    def field_names(cls) -> list[str]:
        if cls._field_names[0] != "context_id":
            cls._field_names.insert(0, "context_id")
        return super().field_names()

    @property
    def context_id(self) -> bytes:
        r"""The primary key of this item."""
        return self._context_id

    @property
    def output_name(self) -> str:
        r"""The name of the field that the contents of the column belong to."""
        raise NotImplementedError

    @property
    def output_type(self) -> Any:
        r"""The data type found in the column that this context is related to."""
        raise NotImplementedError
