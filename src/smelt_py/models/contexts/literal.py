#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any

from ..context import Context


class Literal(Context):
    r"""A Context with constant predetermined output name and type."""

    _name_field = ""
    _data_type = Any

    @property
    def output_name(self) -> str:
        return self._name_field

    @property
    def output_type(self) -> Any:
        return self._data_type
