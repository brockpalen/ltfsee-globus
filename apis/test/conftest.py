"""Common fixtures and options needed for unit tests."""
import pytest

from core.eeadm.file_state import LtfseeFile
from ltfsee_globus import app


@pytest.fixture(scope="module")
def client():
    """Create flask http tester client_id."""
    tester = app.test_client()

    yield tester


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


@pytest.fixture(scope="module")
def flask_context():
    """create flask app context for tests that need that"""
    # http://stackoverflow.com/questions/17375340/testing-code-that-requires-a-flask-app-or-request-context

    ctx = app.app_context()
    ctx.push()

    yield ctx
