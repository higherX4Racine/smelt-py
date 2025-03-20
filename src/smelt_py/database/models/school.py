#  Copyright (C) 2025 by Higher Expectations for Racine County

from dataclasses import dataclass, field

from ..keys import UniqueKey


@dataclass
class School:
    r"""A table of information about a school.

    Parameters
    ----------
    full_name: str
        The full name of the school
    nick_name: str
        An abbreviated version of the school's name.
    school_id: UniqueKey
        The primary key for this item
    """

    full_name: str
    nick_name: str
    school_id: UniqueKey = field(default_factory=UniqueKey.new)
