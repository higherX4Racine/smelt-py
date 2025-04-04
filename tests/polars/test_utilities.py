#  Copyright (c) 2025 by Higher Expectations for Racine County

from polars import col

from smelt_py.polars.utilities import as_filter_expressions


def test_as_filter_expressions():
    for actually_is, should_be in zip(as_filter_expressions({
        "word": "to your Momma",
        "pi": 3.14159
    }),
            [col("word") == "to your Momma",
             col("pi") == 3.14159]):
        assert actually_is.meta.eq(should_be)
