from .output_rule import OutputRule
from .literal import Literal
from .passthrough import Passthrough
from .lookup import Lookup


class Builder:
    def __init__(self, capture_names: list[str]):
        self._keys = capture_names

    def build(self, method: str, value: str, **kwargs) -> OutputRule:
        if method == "literal":
            return Literal(value)
        index = self._keys.index(value) + 1
        if method == "passthrough":
            return Passthrough(index)
        if method == "lookup":
            return Lookup(index, **kwargs)
        raise ValueError(f"invalid output rule method: '{method}'")

    def from_json(self, parsed_json: dict) -> OutputRule:
        return self.build(**parsed_json)
