#  Copyright (c) 2025 by Higher Expectations for Racine County
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .base import Base


@dataclass
class Context(Base):
    context_id: bytes = field(default_factory = lambda: uuid4().bytes)
    r"""Data extracted from the heading of a column.

    Parameters
    ----------
    context_id: bytes
        The primary key of this item, optional. Defaults to `uuid.uuid4()`
    """

    @property
    def output_name(self) -> str:
        r"""The name of the field that the contents of the column belong to."""
        raise NotImplementedError

    @property
    def output_type(self) -> Any:
        r"""The data type found in the column that this context is related to."""
        raise NotImplementedError

    @property
    def primary_key(self) -> bytes:
        return self.context_id
