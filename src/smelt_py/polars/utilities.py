#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any

from polars import (
    col,
    lit,
    Expr,
)


def as_filter_expressions(criteria: dict[str, Any],
                          fields: list[str] = None) -> list[Expr]:
    if fields is None:
        fields = criteria.keys()
    return [col(n) == lit(criteria[n]) for n in fields]

