#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Any, Callable


class Converter:
    r"""Cast a string into a Python type.

    Parameters
    ----------
    functor: Callable[[str], Any]
        the actual function, possibly `int` or `float`
    example: Any
        a prototype of the kind of value emitted by `functor`
    """

    def __init__(self, functor: Callable[[str], Any], example: Any):
        self._functor = functor
        self._example = example

    @property
    def example(self) -> Any:
        return self._example

    @property
    def type(self) -> type:
        r"""The Python type created when this instance parses a string."""
        return type(self._example)

    def __call__(self, text: str) -> Any:
        r"""Parse a string representation into a Python value.

        Parameters
        ----------
        text: str
            Some string representation of a Python value

        Returns
        -------
        Any: a valid Python value

        Examples
        --------
        con = Converter(int, 42)
        con("-1")
        """
        return self._functor(text)

    @classmethod
    def for_built_in(cls, built_in: type) -> "Converter":
        return cls(*BUILT_INS[built_in])


BUILT_INS = {
    bool: (lambda text: False if text == r"False" else bool(text),
           True),
    int: (int, 42),
    float: (float, 3.14),
    str: (str, r"example")
}
