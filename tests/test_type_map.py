#  Copyright (c) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.type_map import (
    Capture,
    Converter,
    TypeMap,
)


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


def test_type_map_keys(type_map):
    assert type_map.keys == {"bool", "int", "float", "str"}


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
def test_casting_items(type_map, key, data_type, text, answer):
    assert type_map(key, text) == answer
    assert type_map.type(key) == data_type


CAPTURES = [
    Capture("life", "42"),
    Capture("euler", "2.71828"),
    Capture("pi", "3.14"),
    Capture("maybe", "False"),
    Capture("word", "to your momma!")
]

MAPPING = TypeMap(
    life=Converter.for_built_in(int),
    euler=Converter.for_built_in(float),
    pi=Converter.for_built_in(float),
    maybe=Converter.for_built_in(bool),
    word=Converter.for_built_in(str)
)

EXPECTED_VALUES = {
    "life": 42,
    "euler": 2.71828,
    "pi": 3.14,
    "maybe": False,
    "word": "to your momma!"
}


def test_typed_captures():
    assert MAPPING.typed_captures(CAPTURES) == EXPECTED_VALUES


@pytest.mark.parametrize("capture", CAPTURES)
def test_casting_captures(capture):
    assert MAPPING.cast(capture) == (capture.name, EXPECTED_VALUES[capture.name])
