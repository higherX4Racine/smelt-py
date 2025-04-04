#  Copyright (c) 2025 by Higher Expectations for Racine County
from dataclasses import dataclass
import pytest
from polars import (
    Binary,
    Int16,
    Float32,
    Schema,
)

from smelt_py.models import BaseModel
from smelt_py.polars.model_framer import ModelFramer


@pytest.mark.parametrize("schema", [
    {"a": Int16, "b": Binary, "c": Float32},
    {},
    {"foo": Binary, "bar": Int16, "baz": Float32}
])
def test_initializing_frame(schema):
    f = ModelFramer(BaseModel, schema)
    assert f.frame.schema == Schema(schema)


def test_model_frame_behavior():
    @dataclass
    class Example(BaseModel):
        foo: bytes
        bar: float
        baz: int

    framer = ModelFramer(Example,
                         {
                            "foo": Binary,
                            "bar": Float32,
                            "baz": Int16
                        })

    assert framer.frame.height == 0
    candidate = Example(b"hi", 3.14, 42)
    new_candidate = Example(b"hi", 2.718, -1)

    result = framer.find_or_append(candidate.as_dict())
    assert result.as_tuple() == pytest.approx(candidate.as_tuple())
    assert framer.frame.height == 1

    result = framer.find_or_append(new_candidate.as_dict(), ["foo"])
    assert result.as_tuple() == pytest.approx(candidate.as_tuple())
    assert framer.frame.height == 1

    result = framer.find_or_append(new_candidate.as_dict())
    assert result.as_tuple() == pytest.approx(new_candidate.as_tuple())
    assert framer.frame.height == 2

    assert framer.frame["foo"].to_list() == [b"hi", b"hi"]
    assert framer.frame["bar"].to_list() == pytest.approx([3.14, 2.718])
    assert framer.frame["baz"].to_list() == [42, -1]

    boring = framer.sanitize_blobs()
    assert boring["foo"].to_list() == [b"hi".hex(), b"hi".hex()]
    assert boring["bar"].to_list() == pytest.approx([3.14, 2.718])
    assert boring["baz"].to_list() == [42, -1]
