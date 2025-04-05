#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any

import pytest

from smelt_py.parsing.parser import Parser, Pattern, TypeMap
from smelt_py.parsing import Element
from smelt_py.parsing.converters import BuiltInConverter


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
    p = Pattern(elements, r"\s")
    del pairs["quantity"]
    m = TypeMap(**pairs)

    with pytest.raises(ValueError) as e:
        _ = Parser(mapping=m, pattern=p)

    assert "The mapping's keys must include all of the pattern's names." in str(e)


@pytest.mark.parametrize("text,number,anything,quantity", [
    ("3 pluribus 1.0", 3, "pluribus", 1.0),
    ("42 exceeds 48.", 42, "exceeds", 48.0),
    ("3 is_three_more_than .14", 3, "is_three_more_than", 0.14),
    ("0 equals 0", 0, "equals", 0.0)
])
def test_parsing(elements, pairs, text, number, anything, quantity):
    p = Parser(mapping=TypeMap(**pairs),
               pattern=Pattern(elements, r"\s"))
    captures = p(text)
    assert captures["number"] == number
    assert captures["anything"] == anything
    assert captures["quantity"] == quantity


def test_no_match(pairs, elements):
    p = Parser(mapping=TypeMap(**pairs),
               pattern=Pattern(elements, r"\s"))
    assert p("") is None
