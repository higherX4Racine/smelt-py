#  Copyright (c) 2025 by Higher Expectations for Racine County

from polars import col, DataFrame

from smelt_py.database.models import BaseModel
from smelt_py.polars import as_filter_expressions, as_row

CAPTURES = {
    "word": "to your Momma",
    "pi": 3.14159
}


def test_as_filter_expressions():
    for actually_is, should_be in zip(as_filter_expressions(CAPTURES),
                                      [col("word") == "to your Momma",
                                          col("pi") == 3.14159]):
        assert actually_is.meta.eq(should_be)


def test_as_row():
    class Example(BaseModel):
        _field_names = ["word", "pi"]

        def __init__(self, word: str, pi: float):
            self.word = word
            self.pi = pi

    example = Example(**CAPTURES)

    frame = DataFrame(CAPTURES)

    assert as_row(example, frame).equals(frame)
