#  Copyright (c) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass, fields, asdict, astuple
from typing import Any


@dataclass
class Base:

    @classmethod
    def field_names(cls) -> list[str]:
        return [f.name for f in fields(cls)]

    @classmethod
    def schema(cls) -> dict[str, Any]:
        return {f.name: f.type for f in fields(cls)}

    def as_tuple(self) -> tuple:
        return astuple(self)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
