#  Copyright (c) 2025 by Higher Expectations for Racine County

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
        context.output_name
    with pytest.raises(NotImplementedError):
        context.output_type
    assert context.as_tuple() == (uid,)
    assert context.as_dict() == {"context_id": uid}


def test_data_tuples():
    class Temp(Context):
        _field_names = ["name", "number"]

        def __init__(self, name: str, number: int, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = name
            self.number = number

    temp = Temp("hi", 42, b"1")
    assert temp.as_tuple() == (b"1", "hi", 42)
    assert temp.as_dict() == dict(context_id=b"1", name='hi', number=42)
