#  Copyright (c) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass

from polars import String, Int16, UInt8, Binary

import pytest

from smelt_py.models import LiteralContext, LookupContext
from smelt_py.polars.context_framer import ContextFramer


@dataclass
class LiteralClass(LiteralContext):
    name: str = None
    rank: int = None
    _name_field = "result"
    _data_type = int


def test_literal_framer():
    literal_framer = ContextFramer(LiteralClass,
                                   {
                                       "name": String,
                                       "rank": UInt8
                                   })

    assert literal_framer.frame.height == 0

    context = literal_framer.find_or_append({
        "context_id": b"deadbeef",
        "name": "hello",
        "rank": 99
    })
    assert context.primary_key == b"deadbeef"
    assert context.name == "hello"
    assert context.rank == 99
    assert context.output_name == "result"
    assert context.output_type == int


@dataclass
class CustomLookup(LookupContext):
    field: str = None
    count: int = None
    _name_field = "field"
    _mapping = {
        "foo": int,
        "bar": float,
        "baz": bool
    }


@pytest.mark.parametrize("field,data_type", [
    ("foo", int),
    ("bar", float),
    ("baz", bool)
])
def test_lookup_framer(field, data_type):
    lookup_framer = ContextFramer(CustomLookup,
                                  {
                                      "field": String,
                                      "count": UInt8
                                  })

    assert lookup_framer.frame.height == 0

    context = lookup_framer.find_or_append({
        "context_id": b"deadbeef",
        "field": field,
        "count": 99
    })
    assert context.primary_key == b"deadbeef"
    assert context.field == field
    assert context.count == 99

    assert context.output_name == field
    assert context.output_type == data_type
