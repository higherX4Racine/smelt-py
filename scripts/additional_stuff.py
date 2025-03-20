from importlib.resources import files
from json import load as json_load
import os

import polars as pl

from smelt_py import HeadingParser, HeadingTracker, PrimaryKeyPlan

DATA_DIR = os.path.join(os.path.expanduser("~"),
                        "Documents",
                        "Data",
                        )

OUTPUT_DIR = os.path.join(DATA_DIR, "Iterations")

PANORAMA_DOWNLOAD_DIR = os.path.join(DATA_DIR,
                                     "Downloads",
                                     "Racine Unified",
                                     "Early Literacy Continuous Improvement",
                                     "2024-25",
                                     "Panorama")

STARBUCK_FILE = os.path.join(PANORAMA_DOWNLOAD_DIR,
                             "StarbuckInternationalSchool_students_ELA_YTD_20250211090449.csv")

starbuck_schema = pl.scan_csv(STARBUCK_FILE).collect_schema()

HEADING_PATH = files("smelt_py").joinpath("data", "panorama_headings.json")
with HEADING_PATH.open("r") as fh:
    raw_rules = json_load(fh)

PARSERS = {
    k: HeadingParser.from_json(v) for k, v in raw_rules.items()
}

del fh

tracker = HeadingTracker(PrimaryKeyPlan("pk"))

for catalog, table in PARSERS.items():
    for column, heading in enumerate(starbuck_schema.names()):
        pk, name, datatype = table.process_heading(heading)
        if datatype is not None:
            tracker.add_appearance("starbuck",
                                   column=column,
                                   catalog=catalog,
                                   key=pk,
                                   output_name=name,
                                   datatype=datatype)

starbuck_schema = pl.Schema(
    dict(
        tracker
        .headings
        .filter(
            pl.col("source") == "starbuck"
        )
        .sort(
            "column"
        ).
        select(
            pl.col("catalog_pk").bin.encode("hex"),
            "datatype"
        )
        .iter_rows()
    )
)

starbuck_raw = (
    pl.read_csv(
        STARBUCK_FILE,
        has_header=False,
        skip_rows=1,
        schema=starbuck_schema,
        row_index_name="row",
        ignore_errors=True
    )
)


def stack_like_columns(columns: list[str], name: str) -> pl.DataFrame:
    pk_name = f"pk_{name}"
    return (
        starbuck_raw
        .unpivot(
            on=columns,
            index="row",
            value_name=name,
            variable_name=pk_name
        )
        .with_columns(
            pl.col(pk_name).str.decode("hex")
        )
    )


grouped_headings = (
    tracker
    .headings
    .group_by(
        "source",
        "catalog",
        "output_name"
    )
    .agg(
        pl.col("catalog_pk").bin.encode("hex")
    )
    # .group_by(
    #     "source",
    #     "catalog"
    # )
    # .agg(
    #     columns=(
    #         pl.struct(
    #             name="output_name",
    #             cols="catalog_pk"
    #         )
    #         .map_elements(
    #             lambda x: stack_like_columns(x["cols"], x["name"]),
    #             return_dtype=pl.Object
    #         )
    #     )
    # )
)

# mapped_headings = (
#     grouped_headings
#     .with_columns(
#         pl.col("columns")
#         .list
#         .eval(
#             pl.element()
#             .map_elements(
#                 lambda s: pmap(s["output_name"],
#                                s["column"]),
#                 return_dtype=pl.Object
#             )
#         )
#     )
# )
# starbuck_tables = [
#     starbuck_raw
#     .unpivot(
#         on=columns,
#         index="row",
#         value_name=output_name
#     )
#     .select(
#         pl.lit(catalog).alias("catalog"),
#         "row",
#         output_name,
#     )
#     for _, catalog, output_name, columns in grouped_headings.iter_rows()
# ]
# catalogs = {
#     k: tracker
#     .headings
#     .select(
#         "catalog",
#         pl.col("catalog_pk").alias("pk"),
#         "source",
#         pl.col("column").alias("index"),
#         pl.col("output_name").alias("name"),
#         "datatype"
#     )
#     .join(
#         v.parsed_headings,
#         on="pk"
#     )
#     .select(
#         ~cs.by_name("pk")
#     ) for k, v in
#     PARSERS.items()
# }
#
# columns = {
#     k: [
#         f"column_{i + 1}"
#         for i in
#         v.get_column("index").to_list()
#     ] for k, v in
#     catalogs.items()
# }
#
# starbuck_tables = {
#     k: starbuck_raw.select(["row"] + v)
#     for k, v in
#     columns.items()
# }
#
# (
#     starbuck_raw
#     .with_columns(
#         pl.col(pl.Binary).bin.encode("hex")
#     )
#     .write_csv(
#         os.path.join(OUTPUT_DIR, "starbuck", "data.csv")
#     )
# )
#
# for name, table in starbuck_tables.items():
#     (
#         table
#         .with_columns(
#             pl.col(pl.Binary).bin.encode("hex")
#         )
#         .write_csv(
#             os.path.join(OUTPUT_DIR, "starbuck", f"{name}.csv")
#         )
#     )
