#  Copyright (c) 2025 by Higher Expectations for Racine County

from typing import NamedTuple

class Capture(NamedTuple):
    r"""A key-value pair of strings extracted by an ``Element``"""
    name: str
    value: str
