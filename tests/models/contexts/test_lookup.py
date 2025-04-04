#  Copyright (c) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass

import pytest

from smelt_py.models.contexts.lookup import Lookup


def test_vanilla_lookup():
    lookup = Lookup()
    with pytest.raises(AttributeError):
        _ = lookup.output_name
    with pytest.raises(AttributeError):
        _ = lookup.output_type


def test_custom_lookup():

    @dataclass
    class CustomLookup(Lookup):
        field: str = None
        count: int = None
        _name_field = "field"
        _mapping = {
            "foo": int,
            "bar": float,
            "baz": bool
        }

    hello = CustomLookup(field="foo", count=42, context_id=b"1")
    assert hello.output_name == "foo"
    assert hello.output_type == int
    assert hello.as_tuple() == (b"1", "foo", 42)
    world = CustomLookup(b"2", "baz", 99)
    assert world.output_name == "baz"
    assert world.output_type == bool
    assert world.as_dict() == {
        "context_id": b"2",
        "field": "baz",
        "count": 99
    }
