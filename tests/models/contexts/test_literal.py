#  Copyright (c) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass
from smelt_py.models.contexts.literal import Literal

def test_literal_context():
    @dataclass
    class LiteralClass(Literal):
        name: str = None
        rank: int = None
        _name_field = "result"
        _data_type = int

    literal_instance = LiteralClass(b"1", "hi", 42)

    assert literal_instance.output_name == "result"
    assert literal_instance.output_type == int
    assert literal_instance.as_dict() == {"context_id": b"1", "name": "hi", "rank": 42}
    assert  literal_instance.as_tuple() == (b"1", "hi", 42)
