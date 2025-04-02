#  Copyright (C) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.keys.primary_key import PrimaryKey


def test_base_primary_key():
    with (pytest.raises(NotImplementedError)):
        _ = PrimaryKey().key


class StubKey(PrimaryKey):
    def __init__(self, x: int):
        self._key = b"%d" % x

    @property
    def key(self) -> bytes:
        return self._key


def test_stub_key():
    a = StubKey(1)
    b = StubKey(2)

    assert a <= b
    assert a == a
    assert b >= a

    assert a == b"1"
    assert b == b"2"

    assert a <= b"99"
    assert b >= b"-99"

    assert repr(a) == "b'1'"
    assert repr(b) == "b'2'"