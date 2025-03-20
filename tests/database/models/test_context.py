# Copyright (C) 2025 by Higher Expectations for Racine County

import pytest
from smelt_py.database.models import Context


def test_context(mock_uuid):
    first = Context()
    assert first.context_id == b"1"
    second = Context()
    assert second.context_id == b"2"

    with pytest.raises(NotImplementedError):
        first.output_name

    with pytest.raises(NotImplementedError):
        second.output_type
