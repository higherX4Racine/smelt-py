# Copyright (C) 2025 by Higher Expectations for Racine County

from polars import (
    Binary,
    Boolean,
    Float32,
    Float64,
    Int8,
    Schema,
    String,
)

import pytest

from pysmelt.text_searching import (
    Capture,
    Element,
    Pattern,
    PolarsCaster,
)


@pytest.mark.parametrize("polars_type", [
    Binary,
    Boolean,
    Float32,
    Float64,
    Int8,
    String,
])
def test_to_polars(polars_type):
    assert PolarsCaster.polars_type(polars_type.__name__) == polars_type


@pytest.mark.parametrize("default_type,should_be",[
    (None, String),
    (Float64, Float64),
    (Int8, Int8),
    (String, String),
])
def test_default_type(default_type, should_be):
    assert PolarsCaster.polars_type("", default_type) == should_be


@pytest.fixture(scope="module")
def pattern() -> Pattern:
    return Pattern(
        [
            Element(r"-?\d+", "number", datatype="Int8"),
            Element(r"\w+", "greeting", datatype="String"),
            Element(r"[,.;:]", required=False),
            Element(r"\w+", "subject", datatype="String"),
            Element(r"[.!?]", required=False)
        ],
        r"\s"
    )


def test_to_polars_schema(pattern):
    assert PolarsCaster.to_polars_schema(pattern) == Schema({
        "number": Int8,
        "greeting": String,
        "subject": String,
    })


@pytest.mark.parametrize("literals", [
    [0, "Yo", "dude"],
    [-1, "Hello", "world"],
    [42, "Hi", "Mom"],
    [99, "Who", "dat"],
])
def test_casting(pattern, literals):
    captures = [Capture(k, str(v)) for k, v in zip(pattern.names, literals)]
    schema = PolarsCaster.to_polars_schema(pattern)
    caster = PolarsCaster(schema)
    typed_captures = caster.cast_captures(captures)
    for actually_is, should_be in zip(typed_captures, literals):
        assert actually_is.value == should_be
