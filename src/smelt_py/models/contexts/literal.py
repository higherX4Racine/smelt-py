#  Copyright (c) 2025 by Higher Expectations for Racine County


from typing import Any, ClassVar

from ..context import Context


class Literal(Context):
    r"""A Context with constant predetermined output name and type."""

    _name_field: ClassVar[str] = ""
    _data_type: ClassVar[type] = Any

    @property
    def output_name(self) -> str:
        return self._name_field

    @property
    def output_type(self) -> type:
        return self._data_type
