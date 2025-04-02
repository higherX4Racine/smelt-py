#  Copyright (c) 2025 by Higher Expectations for Racine County

from json import loads
from re import search

import pytest

from smelt_py.element import Element


@pytest.mark.parametrize("pattern", ["", None, ])
def test_empty_pattern(pattern):
    with pytest.raises(ValueError) as e:
        Element(pattern)
    assert "No empty patterns, please!" in str(e)


@pytest.mark.parametrize("pattern,result", [
    (r"foo?", "foo"),
    (r"oo?", "oo"),
    (r".o+(lish)?", "foolish"),
    (r"(useful)?ness", "ness"),
])
def test_unnamed_required_patterns(pattern, result):
    e = Element(pattern=pattern)
    r = e.render()
    assert r == f"(?:{pattern})"
    m = search(r, "shear foolishness")
    assert m.group(0) == result


@pytest.mark.parametrize("name,pattern,result", [
    ("a", r"foo?", "foo"),
    ("b", r"oo?", "oo"),
    ("c", r".o+(lish)?", "foolish"),
    ("d", r"(useful)?ness", "ness"),
])
def test_named_required_patterns(name, pattern, result):
    e = Element(pattern=pattern, name=name)
    r = e.render()
    assert r == f"(?P<{name}>{pattern})"
    m = search(r, "shear foolishness")
    assert m[name] == result


@pytest.mark.parametrize("name,required,rendering", [
    ("greeting", True, r"(?P<greeting>hi)"),
    ("greeting", False, r"(?P<greeting>(?:hi)?)"),
    (None, True, r"(?:hi)"),
    (None, False, r"(?:hi)?")
])
def test_naming_and_requiring(name, required, rendering):
    e = Element(pattern="hi", name=name, required=required)
    assert e.is_required == required
    assert (not e.is_optional) == required
    assert e.should_discard == (not bool(name))
    assert e.pattern == "hi"
    assert e.render() == rendering


@pytest.mark.parametrize("pattern,value", [
    (r"True|False", True),
    (r"[0-9.]+", 3.14159),
    (r"\d+", 3),
    (r"\w+$", "foosball")
])
def test_parsing(pattern, value):
    e = Element(name="foo", pattern=pattern)
    m = search(e.render(), "True3.14159 foosball")
    assert m["foo"] == str(value)


@pytest.mark.parametrize("json_string,should_be", [
    (
        r"""{"pattern": "NWEA MAP"}""",
        Element(pattern=r"NWEA MAP")
    ),
    (
        r"""{"name": "ScoreType","pattern": "Growth","datatype": "String"}""",
        Element(name="ScoreType", pattern=r"Growth")
    ),
    (
        r"""{"name": "Year","pattern": "\\b\\d+\\b","datatype": "Int16"}""",
        Element(r"\b\d+\b", "Year")
    ),
    (
        r"""{"name": "Version","pattern": "V\\d","optional": true,"datatype": "String"}""",
        Element(r"V\d", name="Version", required=False)
    ),
])
def test_element_from_json(json_string, should_be):
    element = Element.from_json(loads(json_string))
    assert element.name == should_be.name
    assert element.should_discard == should_be.should_discard
    assert element.pattern == should_be.pattern
    assert element.is_required == should_be.is_required
