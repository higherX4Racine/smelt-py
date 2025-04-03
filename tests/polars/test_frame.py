#  Copyright (c) 2025 by Higher Expectations for Racine County
import pytest
from polars import Binary, Int16, Float32, Schema

from smelt_py.polars.model_frame import ModelFrame, BaseModel


@pytest.mark.parametrize("schema", [
    {"a": Int16, "b": Binary, "c": Float32},
    {},
    {"foo": Binary, "bar": Int16, "baz": Float32}
])
def test_initializing_frame(schema):
    f = ModelFrame(schema)
    assert f.frame.schema == Schema(schema)


class Example(BaseModel):
    _field_names = ["foo", "bar", "baz"]

    def __init__(self, foo: str, bar: float, baz: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.foo = foo
        self.bar = bar
        self.baz = baz

