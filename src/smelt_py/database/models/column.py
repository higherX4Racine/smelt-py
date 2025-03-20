#  Copyright (C) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass, field, InitVar

from ..keys import CompositeKey


@dataclass
class Column:
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

    Attributes
    ----------
    column_id: bytes
        The primary key for this item, concatenating `source_id` and `index`

    See Also
    --------
    CompositeKey
    Context
    Source
    """
    context_type: type
    context_id: bytes
    measure_type: type
    source_id: InitVar[bytes]
    index: InitVar[int]
    column_id: CompositeKey = field(init=False)

    def __post_init__(self, source_id: bytes, index: int):
        self.column_id = CompositeKey(source_id, index)

    @property
    def source_id(self) -> bytes:
        return self.column_id.unique_id

    @property
    def index(self) -> int:
        return self.column_id.index
