#  Copyright (C) 2025 by Higher Expectations for Racine County

from uuid import uuid4

from .primary_key import PrimaryKey

class Unique(PrimaryKey):
    r"""A bytes representation of a UUID made via `uuid4`

    Parameters
    ----------
    buffer: bytes
        Usually, a 16-byte representation of a UUID, but any bytes will do.

    See Also
    --------
    uuid4.uuid
    """
    def __init__(self, buffer: bytes):
        self._buffer = bytes(buffer)

    @property
    def key(self) -> bytes:
        return self._buffer

    @classmethod
    def new(cls) -> "Unique":
        return cls(uuid4().bytes)
