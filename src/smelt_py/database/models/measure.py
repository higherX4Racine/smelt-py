#  Copyright (C) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass, field, InitVar
from typing import Self

from ..keys import CompositeKey


@dataclass
class Measure[T]:
    r"""A single typed observation from a parsed table.

    Parameters
    ----------
    column_id: bytes
        A foreign key to the `Column` object that describes this object's context
    row: int
        The zero-indexed row number whence this observation came
    value: T
        A scalar observation

    Attributes
    ----------
    measure_id: CompositeKey
        The primary key of this item, concatenating `column_id` and `row`

    See Also
    --------
    Column
    """
    value: T
    column_id: InitVar[bytes]
    row: InitVar[int]
    measure_id: CompositeKey = field(init=False)

    def __post_init__(self, column_id: bytes, row: int):
        self.measure_id = CompositeKey(column_id, row)

    @property
    def column_id(self) -> bytes:
        return self.measure_id.unique_id

    @property
    def row(self) -> int:
        return self.measure_id.index

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
    def type(self: Self) -> type:
        return type(self.value)
