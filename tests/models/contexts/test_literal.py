#  Copyright (c) 2025 by Higher Expectations for Racine County

from smelt_py.models.contexts.literal import Literal

def test_literal_context():
    class LiteralClass(Literal):
        _field_names = ["name", "rank"]
        _name_field = "result"
        _data_type = int
        def __init__(self, name, rank, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.name = name
            self.rank = rank

    literal_instance = LiteralClass("hi", 42, b"1")

    assert literal_instance.output_name == "result"
    assert literal_instance.output_type == int
    assert literal_instance.as_dict() == {"context_id": b"1", "name": "hi", "rank": 42}
    assert  literal_instance.as_tuple() == (b"1", "hi", 42)
