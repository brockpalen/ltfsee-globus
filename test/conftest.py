"""Common fixtures and options needed for unit tests."""
import importlib

import pytest

from core.eeadm.file_state import LtfseeFile
from ltfsee_globus import create_app


@pytest.fixture(scope="function")
def app(monkeypatch):
    """Create flask application."""
    # reload the config object everytime as the enviornment might change
    monkeypatch.setenv("AUTH_KEY", "my_secret")
    import config

    importlib.reload(config)
    app = create_app(config=config)
    yield app


@pytest.fixture(autouse=True)
def reload_config(monkeypatch):
    """Setup required environment for testing for all tests."""
    monkeypatch.setenv("AUTH_KEY", "my_secret")


@pytest.fixture
def valid_auth_headers():
    """Headers to pass along with the test client to auth as the RMP."""
    headers = {"X-API-KEY": "my_secret"}
    return headers


@pytest.fixture
def invalid_auth_headers():
    """Headers to pass along with the test client to auth as the RMP."""
    headers = {"X-API-KEY": "invalid_secret"}
    return headers


# @pytest.fixture  # can't be fixture see:
# https://github.com/pytest-dev/pytest/issues/349
def migrated_file_single():
    """LtfseeFile example in migrated state."""
    files = [
        LtfseeFile(state="M", replicas=1, tapes=[], path="/gpfs/gpfs0/sample_file2"),
    ]

    return files


# @pytest.fixture  # can't be fixture see:
# https://github.com/pytest-dev/pytest/issues/349
def premigrated_file_single():
    """Attempt LtfseeFile example in premigrated state."""
    files = [
        LtfseeFile(state="P", replicas=2, tapes=[], path="/gpfs/gpfs0/sample_file"),
    ]

    return files


# @pytest.fixture  # can't be fixture see:
# https://github.com/pytest-dev/pytest/issues/349
def resident_file_single():
    """Attempt LtfseeFile example in Resident state."""
    files = [
        LtfseeFile(state="R", replicas=0, tapes=[], path="/gpfs/gpfs0/sample_file3"),
    ]

    return files


# @pytest.fixture  # can't be fixture see:
# https://github.com/pytest-dev/pytest/issues/349
def error_file_single():
    """Attempt LtfseeFile example in Resident state."""
    files = [
        LtfseeFile(state="E", replicas=0, tapes=[], path="/gpfs/gpfs0/sample_file3"),
    ]

    return files


@pytest.fixture()
def flask_context(monkeypatch):
    """create flask app context for tests that need that"""
    # http://stackoverflow.com/questions/17375340/testing-code-that-requires-a-flask-app-or-request-context
    monkeypatch.setenv("AUTH_KEY", "my_secret")
    import config

    importlib.reload(config)
    app = create_app(config=config)

    ctx = app.app_context()
    ctx.push()

    yield ctx
