#  Copyright (c) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.parsing.converter import Converter


@pytest.mark.parametrize("datatype,example,text,answer", [
    (bool, True, "False", False),
    (int, 42, "-1", -1),
    (float, 3.14, "2.71828", 2.71828),
    (str, "example", "identity", "identity")
])
def test_converter(datatype, example, text, answer):
    con = Converter.for_built_in(datatype)
    assert con.type == datatype
    assert con.example == example
    assert con(text) == answer
