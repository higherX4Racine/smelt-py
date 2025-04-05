#  Copyright (c) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.parsing.converters.month import (
    Month as MonthConverter,
    ONE_DIGIT_MONTHS,
    TWO_DIGIT_MONTHS,
    MONTH_NAMES
)


@pytest.mark.parametrize("language", [
    "en",
    "es"
])
def test_month_numbers(language):
    converter = MonthConverter(language)
    assert converter.type == int
    month_maps = [
        TWO_DIGIT_MONTHS,
        {m: i + 1 for i, m in enumerate(MONTH_NAMES[language])},
        ONE_DIGIT_MONTHS,
    ]
    for month_map in month_maps:
        keys = list(month_map.keys())
        should_be = [month_map[key] for key in keys]
        actually = [converter(key) for key in keys]
        assert actually == should_be
