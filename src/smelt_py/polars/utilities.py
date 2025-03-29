#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any

from polars import (
    col,
    lit,
    Expr,
    DataFrame,
)

from ..database.models import BaseModel


def as_filter_expressions(criteria: dict[str, Any],
                          fields: list[str] = None) -> list[Expr]:
    if fields is None:
        fields = criteria.keys()
    return [col(n) == lit(criteria[n]) for n in fields]


def as_row(model_item: BaseModel, template_frame: DataFrame) -> DataFrame:
    return DataFrame([model_item.as_tuple()],
                     schema=template_frame.schema,
                     orient="row")
