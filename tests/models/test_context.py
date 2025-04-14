#  Copyright (c) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass, fields
import pytest

from smelt_py.models.context import Context, Element, Parser

@pytest.mark.parametrize("uid", [
    b"1",
    b"42",
    b"3.14"
])
def test_context(uid):
    context = Context(uid)
    assert context.context_id == uid
    with pytest.raises(NotImplementedError):
        _ = context.output_name
    with pytest.raises(NotImplementedError):
        _ = context.output_type
    assert context.as_tuple() == (uid,)
    assert context.as_dict() == {"context_id": uid}
    assert context.primary_key == uid

@dataclass
class Temp(Context):
    name: str = None
    number: float = None

def test_data_tuples():
    temp = Temp(b"1", "hi", 42)
    assert temp.as_tuple() == (b"1", "hi", 42)
    assert temp.as_dict() == dict(context_id=b"1", name='hi', number=42)
    assert temp.primary_key == b"1"

def test_building_context_type_map():
    assert [f.name for f in fields(Temp)] == ["context_id", "name", "number"]
    type_map = Temp.type_map()
    assert type_map["name"].type == str
    assert type_map["number"].type == float


@pytest.mark.parametrize("text,name,number",[
    ("life 42", "life", 42.0),
    ("pi 3.14", "pi", 3.14),
    ("sub-zero -1", "sub-zero", -1)
])
def test_building_context_parser(text, name, number):
    p = Temp.build_parser([
        Element(r"\S+", "name"),
        Element(r"-?\d+\.?\d*", "number")
    ])

    typed_captures = p.parse(text)

    assert len(typed_captures) == 2
    assert typed_captures["name"] == name
    assert typed_captures["number"] == number