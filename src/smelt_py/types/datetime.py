#  Copyright (c) 2025 by Higher Expectations for Racine County

from datetime import datetime
from smelt_py.parsing.converter import Converter


class DateTime(Converter):
    r"""A converter for parsing datetime strings according to a fixed format.

    Parameters
    fmt: str
        A format specification for `datetime.datetime.strptime`

    See Also
    --------
    datetime.datetime.strptime: a standard text-to-datetime function
    """

    def __init__(self, fmt: str):
        super().__init__(self.interpret,
                         datetime(2025, 3, 15,
                                  11, 12, 13))
        self._format = fmt

    def interpret(self, formatted_date: str) -> datetime:
        r"""Convert the input text to a datetime object."""
        return datetime.strptime(formatted_date, self._format)
