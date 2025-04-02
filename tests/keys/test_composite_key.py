#  Copyright (C) 2025 by Higher Expectations for Racine County

from struct import pack

import pytest

from smelt_py.keys.composite import Composite


@pytest.mark.parametrize("uid,nby,idx", [
    (b"99", 2, 42),
    (b"abcdef0123456789", 16, 4294967295),
    (b"", 0, 99)
])
def test_composite_key(uid, nby, idx):
    composite_key = Composite(uid, idx)

    assert composite_key.key == pack(f">{nby}sI", uid, idx)
    assert composite_key.unique_id == uid
    assert composite_key.index == idx
