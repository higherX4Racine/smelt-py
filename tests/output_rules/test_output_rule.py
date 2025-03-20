from smelt_py.output_rules.output_rule import OutputRule

import pytest

@pytest.mark.parametrize("method", [
    "foo",
    "bar",
    None
])
def test_output_rule(method):
    rule = OutputRule(method)

    assert rule.method == method

    with pytest.raises(NotImplementedError):
        rule(('life', 'means', 42))
