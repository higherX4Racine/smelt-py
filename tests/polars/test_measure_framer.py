#  Copyright (c) 2025 by Higher Expectations for Racine County

from struct import pack

from polars import (
    Binary,
    Datetime,
    Float64,
    Int8,
    Int64,
    String,
    UInt32,
    UInt64, Series,
)

import pytest

from smelt_py.polars.measure_framer import MeasureFramer, Measure


@pytest.mark.parametrize("data_type,values", [
    (Binary, [b"01", b"00", b"beef"]),
    (Datetime(), []),
    (Float64, [3.14, 2.72, 1.41]),
    (Int8, [-1, 0, 1]),
    (Int64, [-32256, 0, 32256]),
    (String, ["low", "medium", "hi there!"]),
    (UInt32, [0, 19999, 323232]),
    (UInt64, [0, 999999, 9999999]),
])
def test_measure_framer(data_type, values):
    framer = MeasureFramer(data_type)
    for r, v in enumerate(values):
        measure = framer.find_or_append({"column_id": b"0x0", "row": r, "value": v})
        assert measure.primary_key == pack(">3sI", b"0x0", r)
        assert measure.value == v
    assert framer.frame.height == len(values)
    assert framer.frame["value"].equals(Series(values, dtype=data_type))
