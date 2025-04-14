#  Copyright (c) 2025 by Higher Expectations for Racine County

from smelt_py.models.outputs.literal import Literal


class LiteralClass(Literal):
    _name_field = "result"
    _data_type = int


def test_literal_context():
    literal_instance = LiteralClass()

    assert literal_instance.output_name == "result"
    assert literal_instance.output_type == int
