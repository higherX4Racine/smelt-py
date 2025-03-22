#  Copyright (c) 2025 by Higher Expectations for Racine County

class Base:

    _field_names = []

    @classmethod
    def field_names(cls) -> list[str]:
        return cls._field_names

    def as_tuple(self) -> tuple:
        return tuple(getattr(self, k) for k in self.field_names())

    def as_dict(self) -> dict:
        return {
            k: getattr(self, k) for
            k in self.field_names()
        }