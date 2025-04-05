#  Copyright (c) 2025 by Higher Expectations for Racine County

from smelt_py.parsing.converters.converter import Converter

def test_converter():
    class Caster:
        def __call__(self, text: str) -> int:
            return 42
        def type(self) -> type:
            return int

    assert isinstance(Caster, Converter)
