#  Copyright (C) 2025 by Higher Expectations for Racine County

class PrimaryKey:
    r"""Descriptor object for tracking unique rows in tables"""

    def __set_name__(self, owner, name):
        self._name = "_" + name

    def __get__(self, instance, owner=None) -> bytes:
        return getattr(instance, self._name)

    def __set__(self, instance, value: bytes | int | str):
        if isinstance(value, bytes):
            pass
        elif isinstance(value, int):
            value = b"%d" % value
        elif isinstance(value, str):
            value = value.encode()
        else:
            raise ValueError("the primary key must be a `bytes`, `int`, or `str`")
        setattr(instance, self._name, value)
