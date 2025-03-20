import re

ENGLISH_MONTHS = {
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'may': 5,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12,
    '01': 1,
    '02': 2,
    '03': 3,
    '04': 4,
    '05': 5,
    '06': 6,
    '07': 7,
    '08': 8,
    '09': 9,
    '1': 1,
    '10': 10,
    '11': 11,
    '12': 12,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
}


def english_months() -> list[str]:
    return [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]


def numeric_months() -> list[str]:
    m = [1 + x for x in range(12)]
    one_digit = [f"{x}" for x in m]
    two_digits = [f"{x:02}" for x in m]
    return sorted(list(
        set(one_digit)
        .union(two_digits)
    ))


def month_as_integer(month_as_text: str) -> int:
    m = re.search(r"^\d+|[a-z]{3}",
                  month_as_text.lower()).group(0)
    return ENGLISH_MONTHS[m]
