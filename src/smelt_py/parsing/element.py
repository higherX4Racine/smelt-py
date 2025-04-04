# Copyright (C) 2025 by Higher Expectations for Racine County
from dataclasses import dataclass


@dataclass
class Element:
    r"""A string pattern to be compiled into part of a regular expression

    Parameters
    ----------
    pattern: str
        A text-matching regular expression without capturing information.
    name: str?
        An optional name, which would mark the element as a capturing group.
    required: bool?
        ``True``, the default, if the pattern must match something.
    """
    pattern: str = ""
    name: str = None
    required: bool = True

    def __post_init__(self):
        if not bool(self.pattern):
            raise ValueError("No empty patterns, please!")
        if self.name is None:
            self.name = ""

    @property
    def is_named(self) -> bool:
        return bool(self.name)

    @property
    def should_discard(self) -> bool:
        return not self.is_named

    @property
    def is_optional(self) -> bool:
        return not self.is_required

    @property
    def is_required(self) -> bool:
        return self.required

    def render(self) -> str:
        r"""A regular expression group which is capturing if ``is_named``"""
        pattern = self.pattern
        if self.should_discard:
            return f"(?:{pattern}){'' if self.is_required else '?'}"
        if self.is_optional:
            pattern = f"(?:{pattern})?"
        return f"(?P<{self.name}>{pattern})"

    @staticmethod
    def from_json(parsed_json: dict) -> "Element":
        return Element(
            pattern=parsed_json["pattern"],
            name=parsed_json.get("name", ""),
            required=not parsed_json.get("optional", False),
        )
