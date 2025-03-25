#  Copyright (c) 2025 by Higher Expectations for Racine County
from sys import prefix

from smelt_py.database.models.base import Base

def test_base_schema():
    class Example(Base):
        _field_names = ["foo", "bar", "baz"]
        def __init__(self, foo: str, bar: float, baz: int, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._foo = foo
            self._bar = bar
            self._baz = baz

        @property
        def foo(self) -> str:
            return self._foo

        @property
        def bar(self) -> float:
            return self._bar

        @property
        def baz(self) -> int:
            return self._baz


    example = Example("pi", 3.14, 3)

    assert example.schema() == {"foo": str, "bar": float, "baz":int}
