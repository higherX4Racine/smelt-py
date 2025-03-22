#  Copyright (c) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.database.models.contexts import LookupContext


def test_vanilla_lookup():
    lookup = LookupContext()
    with pytest.raises(AttributeError):
        lookup.output_name
    with pytest.raises(AttributeError):
        lookup.output_type


def test_custom_lookup():

    class CustomLookup(LookupContext):
        _field_names = ["field", "count"]
        _name_field = "field"
        _mapping = {
            "foo": int,
            "bar": float,
            "baz": bool
        }
        def __init__(self, field: str, count: int, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.field = field
            self.count = count

    hello = CustomLookup(field="foo", count=42, context_id=b"1")
    assert hello.output_name == "foo"
    assert hello.output_type == int
    assert hello.as_tuple() == (b"1", "foo", 42)
    world = CustomLookup("baz", 99, b"2")
    assert world.output_name == "baz"
    assert world.output_type == bool
    assert world.as_dict() == {
        "context_id": b"2",
        "field": "baz",
        "count": 99
    }
