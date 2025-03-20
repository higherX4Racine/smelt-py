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

    CustomLookup = LookupContext.make_subclass(
        "CustomLookup",
        "field",
        {
            "foo": int,
            "bar": float,
            "baz": bool
        },
        [("field", str), ("count", int)]
    )

    hello = CustomLookup(field="foo", count=42)
    assert hello.output_name == "foo"
    assert hello.output_type == int
    world = CustomLookup(field="baz", count=99)
    assert world.output_name == "baz"
    assert world.output_type == bool
