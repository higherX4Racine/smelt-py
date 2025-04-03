#  Copyright (C) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass
import pytest
from smelt_py.keys.primary_key import PrimaryKey


@dataclass(order=True)
class StubKey(PrimaryKey):
    key: PrimaryKey = PrimaryKey()


def test_bad_initialization_of_key():
    with pytest.raises(ValueError) as err:
        StubKey(key=3.14)


def test_stub_key():
    a = StubKey(1)
    b = StubKey(2)

    assert a <= b
    assert a == a
    assert b >= a

    assert b.key == b"2"
    assert a.key == b"1"

    assert a.key <= b"99"
    assert b.key >= b"-99"

    assert repr(a.key) == "b'1'"
    assert repr(b.key) == "b'2'"
