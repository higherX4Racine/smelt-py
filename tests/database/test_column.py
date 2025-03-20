# Copyright (C) 2025 by Higher Expectations for Racine County

from smelt_py.database.models import Column


def test_column():
    column = Column(int, b"99", str, b'42', 42)

    assert column.column_id == b'42\x00\x00\x00*'
    assert column.source_id == b'42'
    assert column.index == 42
    assert column.context_type == int
    assert column.context_id == b'99'
    assert column.measure_type == str
