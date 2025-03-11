from typing import Any

class OutputRule:
    def __init__(self, method: str):
        self._method = method

    @property
    def method(self) -> str:
        return self._method

    def __call__(self, row: tuple) -> Any:
        raise NotImplementedError
