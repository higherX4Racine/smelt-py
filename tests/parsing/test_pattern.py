#  Copyright (c) 2025 by Higher Expectations for Racine County
import os.path
from json import load

import pytest

from smelt_py.parsing.pattern import Element, Pattern


@pytest.fixture(scope="module")
def elements() -> list[Element]:
    return [
        Element(name="foo", pattern=r"\d+"),
        Element(pattern="baz"),
        Element(name="barf", pattern=r"ugh", required=False)
    ]


@pytest.fixture(scope="module")
def pattern(elements) -> Pattern:
    return Pattern(elements, r"[\s:]")


def test_pattern(pattern):
    assert len(pattern) == 2
    assert pattern.names == ["foo", "barf"]


@pytest.fixture(scope="module")
def rendered_pattern() -> str:
    return r"(?P<foo>\d+)[\s:]+(?:baz)[\s:]*(?P<barf>(?:ugh)?)"


def test_rendering(pattern, rendered_pattern):
    assert pattern.render() == rendered_pattern


@pytest.mark.parametrize("string,match,captures", [
    ("42 baz ugh", "42 baz ugh", [("foo", "42"), ("barf", "ugh")]),
    ("42 baz beef", "42 baz ", [("foo", "42"), ("barf", "")]),
    ("42:baz     :ugh", "42:baz     :ugh", [("foo", "42"), ("barf", "ugh")]),
    ("inconceivable", None, None)
])
def test_searching(pattern, string, match, captures):
    m = pattern.search(string)

    if match is not None:
        assert m
        assert len(m.groups()) == len(captures)
        assert m[0] == match
        assert pattern.captures(m) == captures
        assert pattern.extract(string) == captures
    else:
        assert m is None
        assert pattern.extract(string) == []


def test_pattern_from_json():
    with open(os.path.join(os.path.dirname(__file__),
                           "sample_pattern.json"), "r") as fh:
        parsed_json = load(fh)
    p = Pattern.from_json(parsed_json)
    assert p.render() == r"""(?:NWEA MAP)[\s:]+(?P<ScoreType>Growth)[\s:]+(?P<Subject>Math\w*|(Spanish )?Reading)[\s:]+(?P<GradeRange>\S+)[\s:]+(?P<Edition>\S+)[\s:]+(?P<Year>\b\d+\b)[\s:]*(?P<Version>(?:V\d)?)"""
