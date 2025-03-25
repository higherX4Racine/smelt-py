#  Copyright (c) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.parsing.type_map import TypeMap
from smelt_py.parsing import Converter


@pytest.fixture
def converters() -> dict[str, Converter]:
    return {
        k: Converter.for_built_in(v) for k, v in [
            ("bool", bool),
            ("int", int),
            ("float", float),
            ("str", str),
        ]
    }


@pytest.fixture
def type_map(converters) -> TypeMap:
    return TypeMap(**converters)


@pytest.mark.parametrize("key,data_type,text,answer", [
    ("bool", bool, "True", True),
    ("bool", bool, "False", False),
    ("int", int, "42", 42),
    ("int", int, "-1", -1),
    ("float", float, "3.14", 3.14),
    ("float", float, "-0.999", -0.999),
    ("str", str, "howdy", "howdy"),
    ("str", str, "", "")
])
def test_type_map(type_map, key, data_type, text, answer):
    assert type_map(key, text) == answer
    assert type_map.type(key) == data_type
