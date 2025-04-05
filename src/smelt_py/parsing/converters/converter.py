#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Protocol, runtime_checkable


@runtime_checkable
class Converter[T](Protocol):
    r"""A protocol for a callable that can cast strings to other converters."""

    def __call__(self, text: str) -> T:
        r"""Perform the conversion, hopefully more safely than `eval(text)`

        Parameters
        ----------
        text: str
            Some encoding of a Python data type as a string

        Returns
        -------
        T: a concrete instance of the type
        """
        ...

    @property
    def type(self) -> type:
        r"""The type that the instance converts its `str` arguments to"""
        ...
