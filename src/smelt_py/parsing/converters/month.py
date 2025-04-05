#  Copyright (c) 2025 by Higher Expectations for Racine County

from importlib.resources import files
from json import load as json_load
from re import compile, Pattern as RePattern
from typing import ClassVar


class Month:
    MONTH_RE: ClassVar[RePattern] = compile(r"^\d+|[a-z]{3}")

    @staticmethod
    def three_letter_months(language: str):
        r"""TLAs for months in the specified language.

        Parameters
        ----------
        language: str
            the two-letter iso code for the language, e.g. "en" or "es"

        Returns
        -------
        dict[str, int]: a mapping from TLA to numeric month
        """
        return {
            m[:3].lower(): i + 1 for i, m in enumerate(MONTH_NAMES[language])
        }

    def __init__(self, language: str):
        self._map = (
                ONE_DIGIT_MONTHS |
                TWO_DIGIT_MONTHS |
                self.three_letter_months(language)
        )

    def __call__(self, text: str) -> int:
        matches = self.MONTH_RE.search(text.lower())
        month = matches.group(0)
        return self._map.get(month, 127)

    @property
    def type(self) -> type:
        return int


ONE_DIGIT_MONTHS = {
    f"{x}": x for x in range(1, 13)
}

TWO_DIGIT_MONTHS = {
    f"{x:02}": x for x in range(1, 13)
}

with files("smelt_py").joinpath("data", "months.json").open() as fh:
    MONTH_NAMES = json_load(fh)
