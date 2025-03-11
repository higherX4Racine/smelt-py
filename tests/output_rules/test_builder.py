import pytest

from pysmelt.output_rules import OutputRuleBuilder


@pytest.mark.parametrize("method", [
    "foo",
    "bar",
    "baz",
    None
])
def test_bad_method(method):
    builder = OutputRuleBuilder(["a", "b", "c", "ignored"])
    with pytest.raises(ValueError) as err:
        builder.build(method, "ignored")

    assert f"invalid output rule method: '{method}'" in str(err)


@pytest.mark.parametrize("method",[
    "literal",
    "passthrough",
    "lookup"
])
def test_good_methods(method, example_row):
    mapping = dict(a=1, b=0, c="lightspeed")
    names = list(mapping.keys())
    builder = OutputRuleBuilder(names)
    rule = builder.from_json(dict(method=method, value="a", mapping=mapping))
    assert rule.method == method
    if method == "literal":
        assert rule(example_row) == "a"
    if method == "passthrough":
        assert rule(example_row) == example_row[1]
