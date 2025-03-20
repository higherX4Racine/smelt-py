import pytest

from smelt_py.output_rules.lookup import Lookup


@pytest.fixture(scope="module")
def helpful_mapping():
    return {
        "life": "alive",
        "universally": "everywhere",
        "begins": "initial",
        "at": "some place",
        42: "meaning",
        1: "prime",
        2: "secondary",
        3: "tertiary",
        5: "fifth",
        True: "Not wrong",
        b"BEEF": "digital cow",
        "word": "semiotic"
    }


@pytest.mark.parametrize("index", list(range(4)))
def test_lookup(example_row, helpful_mapping, index):
    rule = Lookup(index, helpful_mapping)
    should_be = helpful_mapping[example_row[index]]
    assert rule(example_row) == should_be
