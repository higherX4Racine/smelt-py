# Copyright (C) 2025 by Higher Expectations for Racine County

from datetime import datetime

from smelt_py.database.models import Source


def test_source_creation(mock_uuid):
    now = datetime.now()
    source = Source("some file or another", now, b"42")
    assert source.description == "some file or another"
    assert source.date == now
    assert source.context_id == b"42"
    assert source.source_id == b"1"
