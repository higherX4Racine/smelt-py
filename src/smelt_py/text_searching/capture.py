# Copyright (C) 2025 by Higher Expectations for Racine County

from typing import Any, NamedTuple

class Capture(NamedTuple):
    r"""A key-value pair of strings extracted by an ``Element``"""
    name: str
    value: str


class TypedCapture(NamedTuple):
    r"""A pair with a string key and a class instance value"""
    name: str
    value: Any
