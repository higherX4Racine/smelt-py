#  Copyright (c) 2025 by Higher Expectations for Racine County

from datetime import datetime
import pytest

from smelt_py.parsing.types.datetime import DateTime as DateTimeConverter


@pytest.mark.parametrize("fmt,text,should_be",[
    ("%b %d, %Y %H:%M:%S", "Oct 03, 1977 10:05:00", datetime(1977, 10, 3, 10, 5)),
    ("%Y%m%d%H%M%S", "20250211090206", datetime(2025, 2, 11, 9, 2, 6))
])
def test_datetime_converter(fmt, text, should_be):
    converter = DateTimeConverter(fmt)
    assert converter.example == datetime(2025,3,15,11,12,13)
    assert converter.type == datetime
    assert converter(text) == should_be
