"""Common fixtures and options needed for unit tests."""
import pytest

from ltfsee_globus import app


@pytest.fixture(scope="module")
def client():
    """Create flask http tester client_id."""
    tester = app.test_client()

    yield tester
