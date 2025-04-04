# Copyright (C) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.models.measure import Measure


class CustomObject:
    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
        self._m = x * x + y * y

    @property
    def magnitude(self) -> float:
        return self._m

    def __eq__(self, other):
        return self.magnitude == other.magnitude

    def __lt__(self, other):
        return self.magnitude < other.magnitude

    def __gt__(self, other):
        return self.magnitude > other.magnitude


@pytest.mark.parametrize("lo,hi", [
    (False, True),
    (-1, 42),
    (2.71828, 3.14159),
    ("a", "z"),
    (CustomObject(0, 1), CustomObject(-1, -1))
])
def test_measure(lo, hi):
    m_lo = Measure(b"42", 0, lo)
    assert m_lo.primary_key == b"42\x00\x00\x00\x00"
    assert m_lo.column_id == b"42"
    assert m_lo.row == 0

    m_hi = Measure(b"99", 1, hi)
    assert m_hi.primary_key == b"99\x00\x00\x00\x01"
    assert m_hi.column_id == b"99"
    assert m_hi.row == 1

    assert m_lo == m_lo
    assert m_hi == m_hi
    assert m_lo <= m_hi
    assert m_hi >= m_lo

    assert m_lo != m_hi
