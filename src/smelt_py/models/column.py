#  Copyright (C) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass
from struct import pack

from .base import Base


@dataclass
class Column(Base):
    r"""A dataclass for keeping track of actual columns encountered in a data set

    Parameters
    ----------
    source_id: bytes
        The unique identifier of the column's data source, probably a spreadsheet
    index: int
        The zero-indexed column number in the source
    context_label: str
        The table of Context subclasses that this column's heading belongs to
    context_id: bytes
        The unique identifier of this column's specific Context subclass instance.
    measure_type: type
        The data type of this column's values.

    See Also
    --------
    Context
    Measure
    """
    source_id: bytes
    index: int
    context_label: str
    context_id: bytes
    measure_type: type

    @property
    def primary_key(self) -> bytes:
        return pack(f">{len(self.source_id)}sI",
                    self.source_id,
                    self.index)
