# Copyright (C) 2025 by Higher Expectations for Racine County

from glob import glob
from importlib.resources import files
from json import load as json_load
from os import path

import polars as pl

from smelt_py import HeadingParser

SEPARATOR = r"[\s:]"
HEADING_PATH = files("smelt_py").joinpath("data", "panorama_headings.json")
with HEADING_PATH.open("r") as fh:
    raw_rules = json_load(fh)

del fh

HEADING_RULES = {
    k: HeadingParser.from_json(v) for k, v in raw_rules.items()
}

DATA_PATH = path.join(path.expanduser("~"),
                      "Documents",
                      "Data")

queries = [
    pl
    .scan_csv(dp)
    .select(pl.col("Student Student Number"),
            pl.selectors.matches(HEADING_RULES["el_assessment"]._pattern.render()))
    .unpivot(index="Student Student Number",
             value_name="Observation",
             variable_name="Assessment")
    .filter(~pl.col("Observation").is_null(),
            ~pl.col("Assessment").str.contains("Status"))
    for dp in glob(path.join(
        DATA_PATH,
        "Downloads",
        "Racine Unified",
        "Early Literacy Continuous Improvement",
        "2024-25",
        "Panorama",
        "*.csv"))
]

pl.concat(
    pl.collect_all(
        queries
    )
).write_csv(
    path.join(
        DATA_PATH,
        "Iterations",
        "el_observations_2025-03-05.csv"
    )
)
