# Copyright (C) 2025 by Higher Expectations for Racine County

from json import loads
from re import search

from polars import datatypes
import pytest
from smelt_py.matching.element import Element


@pytest.mark.parametrize("pattern", ["", None, ])
def test_empty_pattern(pattern):
    with pytest.raises(ValueError) as e:
        Element(pattern)
    assert "No empty patterns, please!" in str(e)


@pytest.mark.parametrize("datatype", ["", None, ])
def test_empty_datatype(datatype):
    with pytest.raises(ValueError) as e:
        Element("foo", name="bar", datatype=datatype)
    assert "Named elements must have a datatype." in str(e)


@pytest.mark.parametrize("pattern,result", [
    (r"foo?", "foo"),
    (r"oo?", "oo"),
    (r".o+(lish)?", "foolish"),
    (r"(useful)?ness", "ness"),
])
def test_unnamed_required_patterns(pattern, result):
    e = Element(pattern=pattern)
    assert e.datatype is None
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
    e = Element(pattern=pattern, name=name, datatype="String")
    assert e.datatype == "String"
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
    e = Element(pattern="hi", name=name, required=required, datatype="String")
    assert e.is_required == required
    assert (not e.is_optional) == required
    assert e.should_discard == (not bool(name))
    assert e.pattern == "hi"
    assert e.render() == rendering


@pytest.mark.parametrize("pattern,value,datatype", [
    (r"True|False", True, "Boolean"),
    (r"[0-9.]+", 3.14159, "Float64"),
    (r"\d+", 3, "Int16"),
    (r"\w+$", "foosball", "String")
])
def test_parsing(pattern, value, datatype):
    e = Element(name="foo", pattern=pattern, datatype=datatype)
    m = search(e.render(), "True3.14159 foosball")
    assert m["foo"] == str(value)
    assert getattr(datatypes, e.datatype).to_python()(m['foo']) == value


@pytest.mark.parametrize("json_string,should_be", [
    (
        r"""{"pattern": "NWEA MAP"}""",
        Element(pattern=r"NWEA MAP", datatype="String")
    ),
    (
        r"""{"name": "ScoreType","pattern": "Growth","datatype": "String"}""",
        Element(name="ScoreType", pattern=r"Growth", datatype="String")
    ),
    (
        r"""{"name": "Year","pattern": "\\b\\d+\\b","datatype": "Int16"}""",
        Element(r"\b\d+\b", "Year", datatype="Int16")
    ),
    (
        r"""{"name": "Version","pattern": "V\\d","optional": true,"datatype": "String"}""",
        Element(r"V\d", name="Version", required=False, datatype="String")
    ),
])
def test_element_from_json(json_string, should_be):
    element = Element.from_json(loads(json_string))
    assert element.name == should_be.name
    assert element.should_discard == should_be.should_discard
    assert element.pattern == should_be.pattern
    assert element.is_required == should_be.is_required
    assert element.datatype == should_be.datatype

