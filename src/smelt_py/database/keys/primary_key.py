#  Copyright (C) 2025 by Higher Expectations for Racine County

class PrimaryKey:
    r"""Abstract base class for tracking unique rows in tables"""
    @property
    def key(self) -> bytes:
        r"""A bytes buffer representing a unique row in a table"""
        raise NotImplementedError

    def __eq__(self, other):
        return self.key == other if \
            isinstance(other, bytes) else \
            self.key == other.key

    def __lt__(self, other):
        return self.key < other if \
            isinstance(other, bytes) else \
            self.key < other.key

    def __le__(self, other):
        return not self > other

    def __gt__(self, other):
        return self.key > other if \
            isinstance(other, bytes) else \
            self.key > other.key

    def __ge__(self, other):
        return not self < other

    def __repr__(self):
        return repr(self.key)
