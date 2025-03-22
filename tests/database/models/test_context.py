# Copyright (C) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.database.models import Context


def test_context(mock_uuid):
    first = Context()
    assert first.context_id == b"1"
    second = Context()
    assert second.context_id == b"2"

    with pytest.raises(NotImplementedError):
        first.output_name

    with pytest.raises(NotImplementedError):
        second.output_type

    with pytest.raises(IndexError):
        first.as_tuple()

    with pytest.raises(IndexError):
        first.as_dict()


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
