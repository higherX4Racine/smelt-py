#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import Type


class BuiltIn[T]:
    r"""Cast a string into a built-in type

    Parameters
    ----------
    built_in_type: type
        the result of the casting.
    """

    def __init__(self, built_in_type: Type[T]):
        self._type = built_in_type

    def __call__(self, text: str) -> T:
        return self._type(text)

    @property
    def type(self) -> type:
        return self._type
