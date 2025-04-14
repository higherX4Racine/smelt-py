#  Copyright (c) 2025 by Higher Expectations for Racine County
from collections.abc import Iterable
from dataclasses import dataclass, field, fields
from itertools import islice
from typing import Any
from uuid import uuid4

from .base import Base
from ..parsing.converters import Converter, BuiltInConverter
from ..parsing import Element, Parser

@dataclass
class Context(Base):
    context_id: bytes = field(default_factory=lambda: uuid4().bytes)
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

    @classmethod
    def type_map(cls) -> dict[str, Converter]:
        return {
            f.name: BuiltInConverter(f.type) for
            f in islice(fields(cls), 1, None)
        }

    @classmethod
    def build_parser(cls,
                     elements: Iterable[Element],
                     separator: str = r"[\s:]",
                     **kwargs) -> Parser:
        if not kwargs:
            kwargs = cls.type_map()
        return Parser(elements, separator, **kwargs)