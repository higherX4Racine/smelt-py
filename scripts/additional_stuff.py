from importlib.resources import files
from json import load as json_load
import os

import polars as pl
import polars.selectors as cs

from pysmelt import HeadingParser, HeadingTracker, PrimaryKeyPlan

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

HEADING_PATH = files("pysmelt").joinpath("data", "panorama_headings.json")
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

starbuck_raw = (
    pl.read_csv(
        STARBUCK_FILE,
        has_header=False,
        skip_rows=1,
        schema_overrides=tracker.schema_for("starbuck"),
        row_index_name="row",
        ignore_errors=True
    )
)

catalogs = {
    k: tracker
    .headings
    .select(
        "catalog",
        pl.col("catalog_pk").alias("pk"),
        "source",
        pl.col("column").alias("index"),
        pl.col("output_name").alias("name"),
        "datatype"
    )
    .join(
        v.parsed_headings,
        on="pk"
    )
    .select(
        ~cs.by_name("pk")
    ) for k, v in
    PARSERS.items()
}

columns = {
    k: [
        f"column_{i + 1}"
        for i in
        v.get_column("index").to_list()
    ] for k, v in
    catalogs.items()
}

starbuck_tables = {
    k: starbuck_raw.select(["row"] + v)
    for k, v in
    columns.items()
}

(
    starbuck_raw
    .with_columns(
        pl.col(pl.Binary).bin.encode("hex")
    )
    .write_csv(
        os.path.join(OUTPUT_DIR, "starbuck", "data.csv")
    )
)

for name, table in starbuck_tables.items():
    (
        table
        .with_columns(
            pl.col(pl.Binary).bin.encode("hex")
        )
        .write_csv(
            os.path.join(OUTPUT_DIR, "starbuck", f"{name}.csv")
        )
    )
