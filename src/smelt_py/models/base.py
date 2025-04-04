#  Copyright (c) 2025 by Higher Expectations for Racine County

from dataclasses import fields, asdict, astuple
from typing import Any


class Base:
    r"""A model dataclass inspired by SQLAlchemy and FastAPI."""

    @classmethod
    def field_names(cls) -> list[str]:
        r"""The names of the instance's fields"""
        return [f.name for f in fields(cls)]

    @classmethod
    def schema(cls) -> dict[str, Any]:
        """A mapping from the names of the instance's fields to their types."""
        return {f.name: f.type for f in fields(cls)}

    def as_tuple(self) -> tuple:
        r"""An ordered collection of the instance's field values"""
        return astuple(self)

    def as_dict(self) -> dict[str, Any]:
        r"""A mapping from the names of the instance's fields to their values."""
        return asdict(self)

    @property
    def primary_key(self) -> bytes:
        r"""a unique string of bytes that identifies the instance."""
        raise NotImplementedError
