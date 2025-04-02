#  Copyright (C) 2025 by Higher Expectations for Racine County

from ..keys import CompositeKey
from .base import Base

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

    _field_names = ["column_id", "row", "value"]

    def __init__(self, column_id: bytes, row: int, value: T):
        self._value = value
        self._measure_id = CompositeKey(column_id, row)

    @property
    def value(self) -> T:
        return self._value

    @property
    def measure_id(self) -> bytes:
        r"""The primary key of this item, concatenating `column_id` and `row`"""
        return self._measure_id.key

    @property
    def column_id(self) -> bytes:
        return self._measure_id.unique_id

    @property
    def row(self) -> int:
        return self._measure_id.index

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

    @property
    def type(self) -> type:
        return type(self.value)
