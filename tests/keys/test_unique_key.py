#  Copyright (C) 2025 by Higher Expectations for Racine County

from smelt_py.keys.unique import Unique


def test_unique_key(mock_uuid):
    key = Unique(b"-1")
    assert key.key == b"-1"
    key = Unique.new()
    assert key == b"1"
    assert Unique.new().key == b"2"
