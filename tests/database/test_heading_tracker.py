# Copyright (C) 2025 by Higher Expectations for Racine County

import pytest
from polars import (
    Binary,
    DataFrame,
    DataType,
    Float32,
    Int16,
    Object,
    Schema,
    Series,
    String,
)

from pysmelt.database.heading_tracker import HeadingTracker


@pytest.mark.parametrize("label", [
    "pk",
    "something else"
])
def test_appearance_creation(label, pk_plan_module, mock_uuid):
    appearances = HeadingTracker(pk_plan_module.PrimaryKeyPlan(label))

    assert appearances.headings.columns == [
        label,
        "source",
        "column",
        "catalog",
        "catalog_" + label,
        "output_name",
        "datatype"
    ]

    assert appearances.headings.height == 0


@pytest.fixture(scope="module")
def input_rows() -> list[tuple[str, int, str, bytes, DataType]]:
    return [
        ("foo.csv", 0, "bar", b"11", "aleph", Int16),
        ("foo.csv", 1, "bar", b"21", "aleph", Float32),
        ("foo.csv", 1, "ner", b"13", "bab", Binary),
        ("foo.csv", 2, "ner", b"41", "aleph", String),
        ("baz.csv", 2, "bar", b"15", "bab", Int16),
        ("baz.csv", 2, "bar", b"61", "jin", Float32),
        ("baz.csv", 1, "ner", b"17", "aleph", Binary),
        ("baz.csv", 0, "ner", b"81", "bab", String),
        ("aaa.csv", 0, "bar", b"15", "aleph", Int16),
        ("aaa.csv", 2, "bar", b"61", "bab", Float32),
        ("aaa.csv", 1, "ner", b"17", "aleph", Binary),
        ("aaa.csv", 1, "ner", b"81", "bab", String),
    ]


def test_appearance_behavior(pk_plan_module, mock_uuid, input_rows):
    appearances = HeadingTracker(pk_plan_module.PrimaryKeyPlan("pk"))

    example = DataFrame(input_rows,
                        schema=Schema(dict(
                            source=String,
                            column=Int16,
                            catalog=String,
                            catalog_pk=Binary,
                            output_name=String,
                            datatype=Object
                        )),
                        orient="row")

    example.insert_column(0,
                          Series("pk",
                                 [
                                     str(n).encode("utf8")
                                     for n in range(1, example.height + 1)
                                 ],
                                 Binary))

    for row in input_rows:
        appearances.add_appearance(*row)

    for column in [
        "pk", "source", "column", "catalog", "catalog_pk", "output_name"
    ]:
        assert appearances.headings[column].eq(example[column]).all()

    for actual, should_be in zip(appearances.headings["datatype"],
                                 example["datatype"]):
        assert actual == should_be

    assert appearances.schema_for("foo.csv") == Schema({"column_1": Int16,
                                                        "column_2": String,
                                                        "column_3": String})

    assert appearances.schema_for("baz.csv") == Schema({"column_1": String,
                                                        "column_2": Binary,
                                                        "column_3": String})

    assert appearances.schema_for("aaa.csv") == Schema({"column_1": Int16,
                                                        "column_2": String,
                                                        "column_3": Float32})
