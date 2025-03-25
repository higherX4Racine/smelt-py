# Copyright 2025 by Higher Expectation for Racine County

from polars import (
    DataFrame,
    lit,
    col,
)

from .primary_key_plan import (
    PrimaryKeyPlan,
)
from ..output_rules import (
    OutputRule,
    OutputRuleBuilder,
)
from ..matching import (
    Capture,
    Pattern
)
from .polars_caster import PolarsCaster


class HeadingParser:

    def __init__(self, pattern: Pattern,
                 pk_plan: PrimaryKeyPlan,
                 name_rule: OutputRule,
                 type_rule: OutputRule):
        capture_schema = PolarsCaster.to_polars_schema(pattern)
        self._pattern = pattern
        self._pk_plan = pk_plan
        self._caster = PolarsCaster(capture_schema)
        self._name_rule = name_rule
        self._type_rule = type_rule
        self._headings = DataFrame(
            schema=pk_plan.widen_schema(capture_schema)
        )

    @property
    def parsed_headings(self) -> DataFrame:
        return self._headings

    def process_heading(self, heading: str) -> tuple:
        captures = self._pattern.extract(heading)
        if captures:
            row = self.find_or_add(self._caster.cast_captures(captures))
            return (
                row[0],
                self._name_rule(row),
                self._caster.polars_type(self._type_rule(row))
            )
        return None, None, None

    def find_or_add(self, typed_captures: list[Capture]) -> tuple:
        row = self.find_captures(typed_captures)
        if row.height == 0:
            row = self.make_row(typed_captures)
            self._headings.vstack(row, in_place=True)
        return row.row(0)

    def find_captures(self, typed_captures: list[Capture]) -> DataFrame:
        expressions = [col(k) == lit(v) for k, v in typed_captures]
        return self._headings.filter(*expressions)

    def make_row(self, typed_captures: list[Capture]) -> DataFrame:
        return DataFrame([
            [self._pk_plan.create(), *(v for k, v in typed_captures)]
        ],
            schema=self._headings.schema,
            orient="row"
        )

    @staticmethod
    def from_json(parsed_json: dict) -> "HeadingParser":
        pattern = Pattern.from_json(parsed_json["pattern"])
        rule_builder = OutputRuleBuilder(pattern.names)
        output_rules = parsed_json["outputs"]
        return HeadingParser(
            pattern=pattern,
            name_rule=rule_builder.from_json(output_rules["names"]),
            type_rule=rule_builder.from_json(output_rules["types"]),
            pk_plan=PrimaryKeyPlan(parsed_json["key_label"])
        )
