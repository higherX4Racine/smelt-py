from pysmelt.output_rules.passthrough import Passthrough

import pytest


@pytest.mark.parametrize("index", list(range(5)))
def test_literal(example_row, index):
    rule = Passthrough(index)
    assert rule(example_row) == example_row[index]
