"""Test units for the file_state rest apis."""
import json
from http import HTTPStatus
from unittest.mock import MagicMock

import pytest

import core
from core.eeadm.file_state import LtfseeFile


def test_api_file_state_post(client, monkeypatch):
    """Check that file_state returns expected behavior."""
    data = {"path": "/my/test/path/file.sh"}

    #  "P  2  JD0099JD@POOL_JD@ts4500  MB0355JE@POOL_JE@ts4500  -   -- /gpfs/gpfs0/sample_file",
    #  "M  1  MB0355JE@POOL_JE@ts4500  -                        -   -- /gpfs/gpfs0/sample_file2",
    #  "R  0  -                        -                        -   -- /gpfs/gpfs0/sample_file3",

    mock = MagicMock()
    files = [
        LtfseeFile(state="P", replicas=2, tapes=[], path="/gpfs/gpfs0/sample_file"),
        LtfseeFile(state="M", replicas=1, tapes=[], path="/gpfs/gpfs0/sample_file2"),
        LtfseeFile(state="R", replicas=0, tapes=[], path="/gpfs/gpfs0/sample_file3"),
    ]
    mock.files.return_value = files

    monkeypatch.setattr(core.eeadm.file_state, "EEADM_File_State", mock)

    response = client.post(
        "/api/v0.5/file_state/file_state",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.CREATED  # nosec
