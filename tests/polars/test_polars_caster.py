#  Copyright (c) 2025 by Higher Expectations for Racine County

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

from smelt_py.polars.polars_caster import (
    Capture,
    PolarsCaster,
)

from smelt_py import TypeMap

@pytest.mark.skip
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


@pytest.mark.skip
@pytest.mark.parametrize("default_type,should_be", [
    (None, String),
    (Float64, Float64),
    (Int8, Int8),
    (String, String),
])
def test_default_type(default_type, should_be):
    assert PolarsCaster.polars_type("", default_type) == should_be


@pytest.fixture(scope="module")
def type_map() -> TypeMap:
    return TypeMap(
        number=Int8.to_python,
        greeting=String.to_python,
        subject=String.to_python
    )


@pytest.mark.skip
@pytest.mark.parametrize("literals", [
    [0, "Yo", "dude"],
    [-1, "Hello", "world"],
    [42, "Hi", "Mom"],
    [99, "Who", "dat"],
])
def test_casting(type_map, literals):
    captures = [Capture(k, str(v)) for k, v in zip(type_map.keys, literals)]
    schema = PolarsCaster.to_polars_schema(type_map)
    caster = PolarsCaster(schema)
    typed_captures = caster.cast_captures(captures)
    for actually_is, should_be in zip(typed_captures, literals):
        assert actually_is.value == should_be
