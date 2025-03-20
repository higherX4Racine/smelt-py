import pytest

from smelt_py.parsing import primary_key_plan


@pytest.fixture(scope="package")
def pk_plan_module():
    return primary_key_plan


@pytest.fixture(scope="function")
def mock_uuid(pk_plan_module, monkeypatch):
    class MockUUID:
        count = 0
        @property
        def bytes(self) -> bytes:
            MockUUID.count += 1
            return b"%d" % MockUUID.count

    monkeypatch.setattr(pk_plan_module,
                        "uuid4",
                        MockUUID)
