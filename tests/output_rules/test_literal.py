from smelt_py.output_rules.literal import Literal

import pytest


@pytest.mark.parametrize("value", [
    "shrike",
    "cuckoo",
    "drongo",
    "buzzard"
])
def test_literal(example_row, value):
    rule = Literal(value)
    assert rule(example_row) == value
