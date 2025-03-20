# Copyright 2025 by Higher Expectation for Racine County

from polars import (
    col,
    DataFrame,
    DataType,
    Int16,
    Object,
    Schema,
    String,
)

from .primary_key_plan import PrimaryKeyPlan


class HeadingTracker:
    r"""A polars DataFrame that tracks which headings occur in which sources

    Parameters
    ----------
    pk_plan: PrimaryKeyPlan
        The system for naming and creating the table's primary keys.
    """

    def __init__(self, pk_plan: PrimaryKeyPlan):
        self._pk_plan = pk_plan
        self._headings = DataFrame(
            schema=self.schema()
        )

    def schema(self) -> Schema:
        return self._pk_plan.widen_schema(Schema({
            "source": String,
            "column": Int16,
            "catalog": String,
            "catalog_" + self._pk_plan.label: self._pk_plan.datatype,
            "output_name": String,
            "datatype": Object
        }))

    @property
    def headings(self) -> DataFrame:
        r"""A polars dataframe with six columns

        ``pk_plan.label`` <bytes>
        : the primary key for this table

        source <str>
        : where the heading comes from, probably a file name

        column <int>
        : the zero-indexed column in ``source`` where the heading occurred.

        catalog <str>
        : the ``Catalog`` that holds the heading's parsed contents.

        catalog_``pk_plan.label`` <bytes>
        : the primary key of the heading's row in ``catalog``

        output_name <str>
        : the output field that the column will end up belonging to

        datatype <obj>
        : the type of data found in the cells of this column

        """
        return self._headings

    def add_appearance(self,
                       source: str,
                       column: int,
                       catalog: str,
                       key: bytes,
                       output_name: str,
                       datatype: DataType) -> None:
        self._headings.vstack(
            DataFrame(
                [(self._pk_plan.create(),
                  source,
                  column,
                  catalog,
                  key,
                  output_name,
                  datatype)],
                schema=self.headings.schema,
                orient="row"
            ),
            in_place=True
        )

    def schema_for(self, source: str) -> Schema:
        column_data = (
            self._headings
            .filter(col("source") == source)
            .select("column", "datatype")
            .sort("column")
            .group_by("column",
                      maintain_order=True)
        )
        column_types = {
            f"column_{column + 1}": data["datatype"][0] #noqa
            if data.height == 1 else String
            for (column,), data in column_data
        }
        return Schema(column_types)
