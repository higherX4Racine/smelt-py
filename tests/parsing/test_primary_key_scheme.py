# Copyright (C) 2025 by Higher Expectations for Racine County

import pytest
from polars import Binary, DataFrame, Int8, Schema, String


def test_static_methods(pk_plan_module, mock_uuid):
    assert pk_plan_module.PrimaryKeyPlan.create() == b"1"
    assert pk_plan_module.PrimaryKeyPlan.create() == b"2"
    assert pk_plan_module.PrimaryKeyPlan.datatype == Binary


@pytest.mark.parametrize("label", [None, "", "pk", "indices"])
def test_labelling(pk_plan_module, label):
    should_be = label or "pk"
    scheme = pk_plan_module.PrimaryKeyPlan(label)
    assert scheme.label == should_be


def test_scheming(pk_plan_module, mock_uuid):
    plan = pk_plan_module.PrimaryKeyPlan()
    narrow_schema = Schema({
        "foo": Binary,
        "bar": Int8,
        "baz": String
    })
    wider_schema = plan.widen_schema(narrow_schema)
    assert wider_schema.names() == ["pk", *narrow_schema.names()]
    assert wider_schema.dtypes() == [Binary, *narrow_schema.dtypes()]

    assert plan.widen_schema({}) == Schema({"pk": Binary})


def test_searching(pk_plan_module, mock_uuid):
    plan = pk_plan_module.PrimaryKeyPlan()
    table = DataFrame(
        [
            [plan.create(), plan.create(), plan.create()],
            ["hello", "there", "world"],
            [42, -1, 0]
        ],
        schema={"pk": Binary, "foo": String, "bar": Int8}
    )

    a, b, c = plan.find_row(table, b"1")
    assert a == b"1"
    assert b == "hello"
    assert c == 42

    a, b, c = plan.find_row(table, b"2")
    assert a == b"2"
    assert b == "there"
    assert c == -1

    a, b, c = plan.find_row(table, b"3")
    assert a == b"3"
    assert b == "world"
    assert c == 0

    row = plan.find_row(table, b"BEEF")
    assert row is ()
