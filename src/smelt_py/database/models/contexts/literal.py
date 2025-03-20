#  Copyright (c) 2025 by Higher Expectations for Racine County

from collections.abc import Mapping
from dataclasses import dataclass, make_dataclass
from typing import Any

from ..context import Context


@dataclass
class Literal(Context):
    r"""A Context with constant predetermined output name and type."""

    _name_field = ""
    _data_type = Any

    @property
    def output_name(self) -> str:
        return self._name_field

    @property
    def output_type(self) -> type:
        return self._data_type

    @classmethod
    def make_subclass(cls,
                      class_name: str,
                      output_name: str,
                      output_type: Any,
                      fields: list[tuple[str,Any]|tuple[str,Any,Any]],
                      **kwargs):
        r"""Factory for concrete subclasses of Lookup.

        Parameters
        ----------
        class_name: str
            the name of the new subclass
        output_name: str
            the literal `output_name` for this context.
        output_type: Any
            the literal `output_type` for this context.
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
                '_name_field': output_name,
                '_data_type': output_type
            },
            **kwargs
        )