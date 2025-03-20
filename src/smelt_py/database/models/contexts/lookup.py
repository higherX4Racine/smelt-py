#  Copyright (c) 2025 by Higher Expectations for Racine County

from collections.abc import Mapping
from dataclasses import dataclass, make_dataclass
from typing import Any

from ..context import Context


@dataclass
class Lookup(Context):
    r"""A Context that produces its output name and type from parsed data."""

    _name_field = ""
    _mapping = {}

    @property
    def output_name(self) -> str:
        return getattr(self, self._name_field)

    @property
    def output_type(self) -> type:
        return self._mapping[self.output_name]

    @classmethod
    def make_subclass(cls,
                      class_name: str,
                      name_field: str,
                      mapping: Mapping[str, type],
                      fields: list[tuple[str,Any]|tuple[str,Any,Any]],
                      **kwargs):
        r"""Factory for concrete subclasses of Lookup.

        Parameters
        ----------
        class_name: str
            the name of the new subclass
        name_field: str
            the label of the field that determines the `output_name`
        mapping: Mapping[str, type]
            the rules that connect values of `name_field` to `output_type`
        fields: list[tuple[str,Any]|tuple[str,Any,Any]]
            specifications for other data fields in the context
        kwargs: Mapping
            additional named arguments for `make_dataclass`

        See Also
        --------
        dataclasses.make_dataclass
        """
        return make_dataclass(
            class_name,
            fields=fields,
            bases=(cls,),
            namespace={
                "_mapping": mapping,
                '_name_field': name_field
            },
            **kwargs
        )