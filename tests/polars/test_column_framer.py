#  Copyright (c) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass

from polars import String, Int16, UInt8, Series, Object

import pytest

from smelt_py.models import LiteralContext, LookupContext
from smelt_py.polars import ContextFramer
from smelt_py.polars.column_framer import ColumnFramer, Context


@dataclass
class LiteralClass(LiteralContext):
    name: str = None
    rank: int = None
    _name_field = "result"
    _data_type = int


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


@pytest.fixture(scope="module")
def context_tables():
    contexts = {
        "literal": ContextFramer(LiteralClass,
                                 {"name": String, "rank": Int16}),
        "lookup": ContextFramer(CustomLookup,
                                {"field": String, "count": UInt8})
    }
    for i, n in enumerate(["literally first", "middle", "last"]):
        contexts["literal"].find_or_append({
            "context_id": b"%u" % (i + 1),
            "name": n,
            "rank": i + 1
        })
    for j, f in enumerate(["foo", "bar", "baz"]):
        contexts["lookup"].find_or_append({
            "context_id": b"%u" % j,
            "field": f,
            "count": j
        })
    return contexts


def test_columns_frame(context_tables):
    source_context = Context(b"source")
    columns = ColumnFramer()
    context_count = 0
    for context_key, context_frame in context_tables.items():
        for i in range(context_frame.frame.height):
            context = context_frame[i]
            columns.add_column(source_context, context_count, context_key, context)
            context_count += 1

    assert columns.frame.height == 6
    assert columns.frame["source_id"].equals(Series([b"source"] * 6))
    assert columns.frame["index"].equals(Series([0, 1, 2, 3, 4, 5, ]))
    assert columns.frame["context_label"].equals(
        Series(["literal"] * 3 + ["lookup"] * 3)
    )
    assert columns.frame["context_id"].equals(
        Series([b"1", b"2", b"3", b"0", b"1", b"2", ])
    )
    should_be = (
        Series([int] * 3 + [int, float, bool], dtype=Object)
        .map_elements(repr, return_dtype=String)
    )
    actually_is = (
        columns.frame["measure_type"]
        .map_elements(repr, return_dtype=String)
    )
    assert actually_is.equals(should_be)
