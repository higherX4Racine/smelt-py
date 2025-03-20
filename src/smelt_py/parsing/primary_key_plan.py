# Copyright (C) 2025 by Higher Expectations for Racine County

from uuid import uuid4

from polars import Binary, DataFrame, col, Schema
from polars.exceptions import NoRowsReturnedError


class PrimaryKeyPlan:
    datatype = Binary

    def __init__(self, label: str = None):
        self._label = label or "pk"

    @property
    def label(self) -> str:
        return self._label

    @staticmethod
    def create() -> bytes:
        return uuid4().bytes

    def widen_schema(self, schema: Schema) -> Schema:
        return Schema({self.label: self.datatype} | schema)

    def find_row(self, table: DataFrame, key: bytes) -> tuple:
        try:
            return table.row(
                by_predicate=(col(self._label) == key)
            )
        except NoRowsReturnedError:
            return ()
