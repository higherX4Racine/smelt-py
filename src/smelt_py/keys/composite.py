#  Copyright (C) 2025 by Higher Expectations for Racine County


from struct import pack

from .primary_key import PrimaryKey


class Composite(PrimaryKey):
    r"""Pack a UUID and a 4-byte integer index into a 20-byte buffer.

    Note that this class doesn't actually constrain the size of the bytes
    input. It does truncate or pad the integer into 4 bytes, though.
    Parameters
    ----------
    unique_id: bytes
        The 16-byte representation of a UUID
    index_part: int
        An integer representing a row or column in the source identified by `unique_part`

    See Also
    --------
    struct.pack
    int.from_bytes
    """

    def __init__(self, unique_id: bytes, index_part: int):
        fmt = f">{len(unique_id)}sI"
        self._buffer = pack(fmt, unique_id, index_part)

    @property
    def key(self) -> bytes:
        r"""a >=4-byte, big-endian representation with the integer at the end."""
        return self._buffer

    @property
    def unique_id(self) -> bytes:
        r"""Retrieve the first 16 bytes of a 20-byte composite key"""
        return self._buffer[:-4]

    @property
    def index(self) -> int:
        r"""Retrieve the last 4 bytes as an integer"""
        return int.from_bytes(self._buffer[-4:], "big", signed=False)
