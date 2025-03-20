# Copyright (C) 2025 by Higher Expectations for Racine County

from re import escape
import pytest
from smelt_py.database.models import School


def test_blank_school():
    should_be = escape(r"School.__init__() missing 2 required positional arguments: 'full_name' and 'nick_name'")
    with pytest.raises(TypeError, match=should_be):
        School()


def test_named_school(mock_uuid):
    school = School("Wayside School", "Wayz")
    assert school.school_id == b"1"
    assert school.full_name == "Wayside School"
    assert school.nick_name == "Wayz"