#  Copyright (C) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass, field
from ..keys import UniqueKey


@dataclass
class Context:
    r"""Data extracted from the heading of a column.

    Attributes
    ----------
    context_id: bytes
        The primary key of this item.
    """
    context_id: UniqueKey = field(default_factory=UniqueKey.new, kw_only=True)

    @property
    def output_name(self) -> str:
        r"""The name of the field that the contents of the column belong to."""
        raise NotImplementedError

    @property
    def output_type(self) -> type:
        r"""The data type found in the column that this context is related to."""
        raise NotImplementedError
