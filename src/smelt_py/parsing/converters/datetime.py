#  Copyright (c) 2025 by Higher Expectations for Racine County

from datetime import datetime


class DateTime:
    r"""A converter for parsing datetime strings according to a fixed format.

    Parameters
    fmt: str
        A format specification for `datetime.datetime.strptime`

    See Also
    --------
    datetime.datetime.strptime: a standard text-to-datetime function
    """

    def __init__(self, fmt: str):
        self._format = fmt

    def __call__(self, text: str) -> datetime:
        r"""Convert the input text to a datetime object."""
        return datetime.strptime(text, self._format)

    @property
    def type(self) -> type:
        return datetime
