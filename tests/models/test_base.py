#  Copyright (c) 2025 by Higher Expectations for Racine County
from dataclasses import dataclass
import pytest
from smelt_py.models.base import Base


def test_base_schema():
    @dataclass
    class Example(Base):
        foo: str
        bar: float
        baz: int

    example = Example("pi", 3.14, 3)

    assert example.schema() == {"foo": str, "bar": float, "baz": int}
    assert example.field_names() == ["foo", "bar", "baz"]
    assert example.as_dict() == {"foo": "pi", "bar": 3.14, "baz": 3}
    assert example.as_tuple() == ("pi", 3.14, 3)

    with pytest.raises(NotImplementedError):
        _ = example.primary_key