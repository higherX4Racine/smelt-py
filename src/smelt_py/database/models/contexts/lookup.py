#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any
from ..context import Context


class Lookup(Context):
    r"""A Context that produces its output name and type from parsed data."""

    _name_field = ""
    _mapping = {}

    @property
    def output_name(self) -> str:
        return getattr(self, self._name_field)

    @property
    def output_type(self) -> Any:
        return self._mapping[self.output_name]
