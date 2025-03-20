#  Copyright (C) 2025 by Higher Expectations for Racine County
from dataclasses import dataclass, field
from datetime import datetime

from ..keys import UniqueKey


@dataclass
class Source:
    r"""A description of a downloaded file or fetched blob with Panorama data

    As of 2025, data must be downloaded from Panorama in one CSV sheet per
    school. Consequently, `school_id` is a mandatory foreign key for each
    `Source`.

    Parameters
    ----------
    description: str
        identifying information about the source, like its file name.
    date: datetime
        a timestamp of when the data were pulled from Panorama
    school_id: bytes
        foreign key to the school that the source describes
    source_id : UniqueKey
        The primary key for this item.
    """
    description: str
    date: datetime
    school_id: bytes
    source_id: UniqueKey = field(default_factory=UniqueKey.new)
