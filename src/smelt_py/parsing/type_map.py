#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any

from .converters import Converter
from .capture import Capture


class TypeMap:
    r"""Syntactic sugar for a string-keyed dictionary of parsing functions

    Parameters
    ----------
    kwargs: Converter
        string-keyed functors that convert a string input to another type.
    """

    def __init__(self, **kwargs: Converter):
        self._map = kwargs

    def __call__(self, key: str, value: str) -> Any:
        r"""Convert a string value to a new type.

        Parameters
        ----------
        key: str
            Signifies which type the string should be parsed as.
        value: str
            A literal string that can be parsed as a new value type.

        Returns
        -------
        Any: the exact return type depends upon the `TypeMap`.
        """
        return self._map[key](value)

    def cast(self, capture: Capture) -> tuple[str, Any]:
        r"""Convert the `value` of a capture object according to its name."""
        return capture.name, self.__call__(capture.name, capture.value)

    def type(self, key: str) -> Any:
        r"""The type returned by the `Callable` mapped to `key`."""
        return self._map[key].type

    def convert_captures(self, captures: list[Capture]) -> dict[str, Any]:
        return {
            name: self.__call__(name, value) for
            name, value in
            captures
        }

    @property
    def keys(self) -> set[str]:
        r"""The keys that the instance uses to cast strings to typed objects"""
        return set(self._map.keys())
