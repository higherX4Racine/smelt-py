#  Copyright (C) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass
from struct import pack

from .base import Base


@dataclass
class Measure[T](Base):
    r"""A single typed observation from a parsed table.

    Parameters
    ----------
    column_id: bytes
        A foreign key to the `Column` object that describes this object's context
    row: int
        The zero-indexed row number whence this observation came
    value: T
        A scalar observation

    See Also
    --------
    Column
    """
    column_id: bytes
    row: int
    value: T

    @property
    def primary_key(self) -> bytes:
        return pack(f">{len(self.column_id)}sI",
                    self.column_id,
                    self.row)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return not self > other

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return not self < other
