#  Copyright (C) 2025 by Higher Expectations for Racine County

import pytest

from smelt_py.database.keys import unique


@pytest.fixture(scope="function")
def mock_uuid(monkeypatch):
    class MockUUID:
        count = 0

        @property
        def int(self) -> int:
            MockUUID.count += 1
            return MockUUID.count

        @property
        def bytes(self) -> bytes:
            return b"%d" % self.int

    monkeypatch.setattr(unique,
                        "uuid4",
                        MockUUID)
