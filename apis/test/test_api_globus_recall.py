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
from flask import current_app

import apis
from apis.globus_recall import globus_recall


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

    monkeypatch.setattr(apis.globus_recall, "cached_file_state", moc_con)

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
    [(error_file_single(), "resident", HTTPStatus.INTERNAL_SERVER_ERROR)],
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

    monkeypatch.setattr(apis.globus_recall, "cached_file_state", moc_con)

    response = client.post(
        "/api/v0.5/globus_recall/globus_recall",
        data=json.dumps(data),
        content_type="application/json",
    )

    # we expect only 201 rsponse codes
    logging.debug(f"status_code is {response.status_code}")
    assert response.status_code == httpresp  # nosec


@pytest.mark.parametrize(
    "lib_list,kwargs,calls",
    [
        (
            ["lib2"],
            {"taskid": "535f580c"},
            {"library": "lib2"},
        ),  # single library configured
        (
            ["lib1", "lib2"],
            {"taskid": "535f580c"},
            {"library": "lib1"},
        ),  # multiple lib hash = 0
        (
            ["lib1", "lib2"],
            {"taskid": "535f580b"},
            {"library": "lib2"},
        ),  # multiple lib hash = 1
        (None, {"taskid": "535f580c"}, {}),  # no library given
        (
            None,
            {"taskid": "535f580c", "library": "custom_lib"},
            {"library": "custom_lib"},
        ),  # lib passed
    ],
)
def test_globus_recall_lib_selection(
    flask_context, monkeypatch, lib_list, kwargs, calls
):
    """Validate that it correctly selects libraries based on configuration options."""
    current_app.config["LTFSEE_LIB"] = lib_list
    logging.debug(current_app.config["LTFSEE_LIB"])
    mock = MagicMock()
    monkeypatch.setattr(apis.globus_recall, "EEADM_Recall", mock)

    globus_recall("/gpfs/glues0/file.dat", **kwargs)
    mock.assert_called_once()
    logging.debug(f"EEADM_Recall() called with: {mock.call_args}")
    mock.assert_called_with("/gpfs/glues0/file.dat", **calls)
