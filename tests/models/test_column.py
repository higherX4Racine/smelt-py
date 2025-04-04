# Copyright (C) 2025 by Higher Expectations for Racine County

from smelt_py.models.column import Column


def test_column():
    assert Column.field_names() == [
        "source_id", "index", "context_label", "context_id", "measure_type"
    ]
    column = Column(b"42", 42, "SomeContext", b"99", str)

    assert column.primary_key == b'42\x00\x00\x00*'
    assert column.source_id == b'42'
    assert column.index == 42
    assert column.context_label == "SomeContext"
    assert column.context_id == b'99'
    assert column.measure_type == str
