import pytest

@pytest.fixture(scope="module", params=[
    ["life", "universally", "begins", "at", 42],
    [1, 1, 2, 3, 5],
    [True, b"BEEF", "word", 42, 3.14159],
])
def example_row(request):
    return request.param


