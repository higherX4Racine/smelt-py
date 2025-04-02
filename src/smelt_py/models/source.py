#  Copyright (C) 2025 by Higher Expectations for Racine County

from datetime import datetime

from ..keys import UniqueKey
from .base import Base

class Source(Base):
    r"""A description of a downloaded file or fetched blob with Panorama data

    As of 2025, data must be downloaded from Panorama in one CSV sheet per
    school. Consequently, `context_id` is a mandatory foreign key for each
    `Source`.

    Parameters
    ----------
    description: str
        identifying information about the source, like its file name.
    date: datetime
        a timestamp of when the data were pulled from Panorama
    context_id: bytes
        foreign key to the context that the source describes
    source_id : UniqueKey
        The primary key for this item.
    """

    _field_names = ["source_id", "description", "date", "context_id"]
    def __init__(self, description: str, date: datetime, context_id: bytes, source_id: bytes=None):
        self._description = description
        self._date = date
        self._context_id = context_id
        self._source_id = source_id if \
            source_id is not None else \
            UniqueKey.new().key

    @property
    def source_id(self) -> bytes:
        return self._source_id

    @property
    def description(self) -> str:
        return self._description

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def context_id(self) -> bytes:
        return self._context_id
