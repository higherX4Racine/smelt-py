# Copyright (C) 2025 by Higher Expectations for Racine County

from json import load

from polars import (
    Binary,
    Boolean,
    Float32,
    Float64,
    Int8,
    Schema,
    String,
)

import pytest

from smelt_py.parsing.heading_parser import HeadingParser
from smelt_py.output_rules.literal import Literal as LiteralOutputRule
from smelt_py.output_rules.passthrough import Passthrough as PassthroughOutputRule
from smelt_py.output_rules.lookup import Lookup as LookupOutputRule
from smelt_py.matching import TypedCapture, Element, Pattern


@pytest.fixture(scope="module")
def pattern() -> Pattern:
    return Pattern(
        [
            Element(r"-?\d+", "number", datatype="Int8"),
            Element(r"\w+", "greeting", datatype="String"),
            Element(r"[,.;:]", required=False),
            Element(r"\w+", "subject", datatype="String"),
            Element(r"[.!?]", required=False)
        ],
        r"\s"
    )


@pytest.fixture(scope="function")
def parser(pattern, pk_plan_module, mock_uuid):
    result = HeadingParser(pattern=pattern,
                           pk_plan=pk_plan_module.PrimaryKeyPlan("pk"),
                           name_rule=LiteralOutputRule("greeting"),
                           type_rule=LiteralOutputRule("String"))
    _ = result.find_or_add([
        TypedCapture("number", 0),
        TypedCapture("greeting", "Yo"),
        TypedCapture("subject", "dude")
    ])
    return result


def test_parsed_heading_creation(parser):
    assert parser.parsed_headings.schema == Schema({
        "pk": Binary,
        "number": Int8,
        "greeting": String,
        "subject": String,
    })
    assert parser.parsed_headings.height == 1
    assert parser.parsed_headings["pk"][0] == b"1"
    assert parser.parsed_headings["number"][0] == 0
    assert parser.parsed_headings["greeting"][0] == "Yo"
    assert parser.parsed_headings["subject"][0] == "dude"


@pytest.mark.parametrize("heading,expected_captures", [
    ("-1 Hello, world", (-1, "Hello", "world")),
    ("42 Hi, Mom!", (42, "Hi", "Mom")),
    ("99 Who dat?", (99, "Who", "dat")),
])
def test_capture_functions(parser, pattern, heading, expected_captures):
    captures = pattern.extract(heading)
    typed_captures = parser._caster.cast_captures(captures)
    assert typed_captures == [
        TypedCapture(k, v)
        for k, v in
        zip(["number", "greeting", "subject"],
            expected_captures)
    ]
    found_frame = parser.find_captures(typed_captures)
    assert found_frame.height == 0
    row = parser.find_or_add(typed_captures)
    assert row[0] == b"2"
    assert row[1:] == expected_captures
    found_frame = parser.find_captures(typed_captures)
    assert found_frame.height == 1
    assert found_frame.row(0) == row


def test_a_fixed_case(pk_plan_module, mock_uuid):
    contexts = [
        ("A baz:-1", "A", -1, b"1", String),
        ("D:baz -42", "D", -42, b"4", Boolean),
        ("B:baz:-1", "B", -1, b"2", Float32),
        ("C baz 1", "C", 1, b"3", Binary),
    ]
    pattern = Pattern([
        Element(name="letters", pattern=r"[A-Za-z]", datatype="String"),
        Element(pattern="baz"),
        Element(name="amounts", pattern=r"-?\d+", required=False, datatype="Int8")
    ], r"[\s:]")

    h_p = HeadingParser(pattern,
                        pk_plan_module.PrimaryKeyPlan("pk"),
                        PassthroughOutputRule(1),
                        LookupOutputRule(1, mapping={
                            "A": "String",
                            "B": "Float32",
                            "C": "Binary",
                            "D": "Boolean",
                        }))

    for index in [0, 2, 3]:
        h_p.process_heading(contexts[index][0])

    for heading, letter, amount, index, expected_type in contexts:
        pk, observed_field, observed_type = h_p.process_heading(heading)
        assert observed_field == letter
        assert observed_type == expected_type


def test_no_captures_in_heading(parser):
    a, b, c = parser.process_heading("ZZZZZZZZZZZZZZ")
    assert a is None
    assert b is None
    assert c is None


@pytest.fixture(scope="module")
def parsed_json() -> dict:
    with open("tests/parsing/sample_heading_parser.json", "r") as fh:
        pj = load(fh)
    return pj


def test_building_from_json(parsed_json, pk_plan_module, mock_uuid):
    headings = [
        "Amira ORF - English Dece 2024 Value",
        "Amira ORF - English Janu 2025 Status",
        "Amira ORF - English Janu 2025 Value",
        "Nonsense Words Fall 2023 Status",
        "Nonsense Words Fall 2023 Value",
        "Nonsense Words November 2024 Value",
        "Letter Sounds Sept 2024 Status",
        "Letter Sounds Sept 2024 Value",
        "Letter Sounds November 2024 Value",
        "Letter ID Fall 2023 Status",
        "Letter ID Fall 2023 Value",
        "Letter ID Janu 2025 Value",
    ]

    assessments = ["Amira ORF - English"] * 3 + \
                  ["Nonsense Words"] * 3 + \
                  ["Letter Sounds"] * 3 + \
                  ["Letter ID"] * 3
    months = ["Dece", "Janu", "Janu"] + \
             ["Fall", "Fall", "November"] + \
             ["Sept", "Sept", "November"] + \
             ["Fall", "Fall", "Janu"]
    years = [2024, 2025, 2025] + \
            [2023, 2023, 2024] + \
            [2024] * 3 + \
            [2023, 2023, 2025]
    units = ["Value", "Status", "Value"] + \
            ["Status", "Value", "Value"] * 3
    data_types = [Float64, String, Float64] + \
                 [String, Float64, Float64] * 3
    primary_keys = [
        str(x).encode("utf-8")
        for x in
        range(1, len(data_types) + 1)
    ]

    parser = HeadingParser.from_json(parsed_json)

    answers = [parser.process_heading(h) for h in headings]

    assert parser.parsed_headings["Assessment"].eq(assessments).all()
    assert parser.parsed_headings["Month"].eq(months).all()
    assert parser.parsed_headings["Year"].eq(years).all()
    assert parser.parsed_headings["Unit"].eq(units).all()

    for i, (key, name, datatype) in enumerate(answers):
        assert key == primary_keys[i]
        assert name == units[i]
        assert datatype == data_types[i]
