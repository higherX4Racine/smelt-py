#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any

import pytest

from smelt_py.parsing.parser import Parser, Element, Capture
from smelt_py.parsing.converters import BuiltInConverter, Converter


@pytest.fixture
def elements() -> list[Element]:
    return [
        Element(r"\d+", "number"),
        Element(r"\w+", "anything"),
        Element(r"[+-]?\d*\.?\d*", "quantity")
    ]


@pytest.fixture()
def pairs() -> dict[str, Any]:
    return dict(number=BuiltInConverter(int),
                anything=BuiltInConverter(str),
                quantity=BuiltInConverter(float))


def test_initialization(elements, pairs):
    del pairs["quantity"]

    with pytest.raises(ValueError) as e:
        _ = Parser(elements, r"\s", **pairs)

    assert "The mapping's keys must include all of the pattern's names." in str(e)


@pytest.mark.parametrize("text,number,anything,quantity", [
    ("3 pluribus 1.0", 3, "pluribus", 1.0),
    ("42 exceeds 48.", 42, "exceeds", 48.0),
    ("3 is_three_more_than .14", 3, "is_three_more_than", 0.14),
    ("0 equals 0", 0, "equals", 0.0)
])
def test_parsing(elements, pairs, text, number, anything, quantity):
    p = Parser(elements, r"\s", **pairs)
    captures = p.parse(text)
    assert captures["number"] == number
    assert captures["anything"] == anything
    assert captures["quantity"] == quantity


def test_no_match(pairs, elements):
    p = Parser(elements, r"\s", **pairs)
    assert p.parse("") is None


@pytest.fixture(scope="module")
def converters() -> dict[str, Converter]:
    return {
        k: BuiltInConverter(v) for k, v in [
            ("bool", bool),
            ("int", int),
            ("float", float),
            ("str", str),
        ]
    }

@pytest.fixture(scope="module")
def dummy_parser(converters) -> Parser:
    return Parser([Element(r"\w", name=k) for k in converters.keys()],
                  r" ",
                  **converters)


@pytest.mark.parametrize("key,text,answer", [
    ("bool", "True", True),
    ("bool", "False", True),
    ("bool", "", False),
    ("int", "-1", -1),
    ("int", "42", 42),
    ("float", "3.14", 3.14),
    ("float", "-0.999", -0.999),
    ("str", "howdy", "howdy"),
    ("str", "", ""),
    (Capture("int", "42"), None, 42),
    (Capture("float", "2.71828"), None, 2.71828),
    (Capture("float", "3.14"), None, 3.14),
    (Capture("str", ""), None, ""),
    (Capture("str", "to your momma!"), None, "to your momma!")
])
def test_converting(dummy_parser, key, text, answer):
    if text is None:
        result = dummy_parser.convert(key)
    else:
        result = dummy_parser.convert(key, text)
    assert result == answer
