"""Test units for the globus_recall apis."""
import json
import logging
from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from conftest import (
    error_file_single,
    migrated_file_single,
    premigrated_file_single,
    resident_file_single,
)

import apis


@pytest.mark.parametrize(
    "target_file,state,httpresp",
    [
        (migrated_file_single(), "archived", HTTPStatus.CREATED),
        (premigrated_file_single(), "resident", HTTPStatus.CREATED),
        (resident_file_single(), "resident", HTTPStatus.CREATED),
    ],
)
def test_api_globus_recall_post(client, monkeypatch, target_file, state, httpresp):
    """Check that file_state returns expected behavior."""
    data = {"path": "/my/test/path/file.sh", "globus_taskid": "aaaa-bbbb"}

    #  "P  2  JD0099JD@POOL_JD@ts4500  MB0355JE@POOL_JE@ts4500  -   -- /gpfs/gpfs0/sample_file",
    #  "M  1  MB0355JE@POOL_JE@ts4500  -                        -   -- /gpfs/gpfs0/sample_file2",
    #  "R  0  -                        -                        -   -- /gpfs/gpfs0/sample_file3",
    mock = MagicMock()
    mock.files = target_file

    def moc_con(*args, **kwargs):
        return mock

    monkeypatch.setattr(apis.globus_recall, "EEADM_File_State", moc_con)

    response = client.post(
        "/api/v0.5/globus_recall/globus_recall",
        data=json.dumps(data),
        content_type="application/json",
    )
    json_data = response.get_json()

    # check expected state of a migrated/premigrated/resident file
    logging.debug(f"file state is: {json_data['state']}")
    assert json_data["state"] == state  # nosec

    # we expect only 201 rsponse codes
    logging.debug(f"status_code is {response.status_code}")
    assert response.status_code == httpresp  # nosec


@pytest.mark.parametrize(
    "target_file,state,httpresp",
    [(error_file_single(), "resident", HTTPStatus.INTERNAL_SERVER_ERROR),],
)
def test_api_globus_recall_post_error(
    client, monkeypatch, target_file, state, httpresp
):
    """Check that file_state returns expected behavior."""
    data = {"path": "/my/test/path/file.sh", "globus_taskid": "aaaa-bbbb"}

    #  "P  2  JD0099JD@POOL_JD@ts4500  MB0355JE@POOL_JE@ts4500  -   -- /gpfs/gpfs0/sample_file",
    #  "M  1  MB0355JE@POOL_JE@ts4500  -                        -   -- /gpfs/gpfs0/sample_file2",
    #  "R  0  -                        -                        -   -- /gpfs/gpfs0/sample_file3",
    mock = MagicMock()
    mock.files = target_file

    def moc_con(*args, **kwargs):
        return mock

    monkeypatch.setattr(apis.globus_recall, "EEADM_File_State", moc_con)

    response = client.post(
        "/api/v0.5/globus_recall/globus_recall",
        data=json.dumps(data),
        content_type="application/json",
    )

    # we expect only 201 rsponse codes
    logging.debug(f"status_code is {response.status_code}")
    assert response.status_code == httpresp  # nosec
