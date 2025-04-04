#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Type

from polars import Binary, UInt32

from .model_framer import ModelFramer
from ..models import Measure


class MeasureFramer[T](ModelFramer[T]):
    def __init__(self, data_type: Type[T]):
        super().__init__(Measure,
                         {
                             'column_id': Binary,
                             'row': UInt32,
                             'value': data_type
                         })
