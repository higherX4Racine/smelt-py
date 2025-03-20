#  Copyright (C) 2025 by Higher Expectations for Racine County

from smelt_py.database.keys import UniqueKey


def test_unique_key(mock_uuid):
    key = UniqueKey(b"-1")
    assert key.key == b"-1"
    key = UniqueKey.new()
    assert key == b"1"
    assert UniqueKey.new().key == b"2"
