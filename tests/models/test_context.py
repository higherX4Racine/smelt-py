#  Copyright (c) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass, KW_ONLY
import pytest

from smelt_py.models.context import Context


@pytest.mark.parametrize("uid", [
    b"1",
    b"42",
    b"3.14"
])
def test_context(uid):
    context = Context(uid)
    assert context.context_id == uid
    with pytest.raises(NotImplementedError):
        _ = context.output_name
    with pytest.raises(NotImplementedError):
        _ = context.output_type
    assert context.as_tuple() == (uid,)
    assert context.as_dict() == {"context_id": uid}
    assert context.primary_key == uid


def test_data_tuples():
    @dataclass
    class Temp(Context):
        name: str = None
        number: int = None

    temp = Temp(b"1", "hi", 42)
    assert temp.as_tuple() == (b"1", "hi", 42)
    assert temp.as_dict() == dict(context_id=b"1", name='hi', number=42)
    assert temp.primary_key == b"1"
