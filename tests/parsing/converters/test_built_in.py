#  Copyright (c) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.parsing.converters.built_in import BuiltIn


@pytest.mark.parametrize("datatype,text,answer", [
    (bool, "False", True),
    (bool, "", False),
    (int, "-1", -1),
    (float, "2.71828", 2.71828),
    (str, "identity", "identity")
])
def test_converter(datatype, text, answer):
    con = BuiltIn(datatype)
    assert con.type == datatype
    assert con(text) == answer
