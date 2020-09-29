"""Basic flask functioning tests."""
import json
from http import HTTPStatus

import pytest  # noqa:


def test_flask_install(client):
    """Check that the API page with swagger exists."""
    response = client.get("/api/v0.5/", content_type="html/text")
    assert response.status_code == 200  # nosec


def test_file_state_post(client):
    """Check that file_state returns expected behavior."""
    data = {"path": "/my/test/path/file.sh"}

    response = client.post(
        "/api/v0.5/file_state/file_state",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.CREATED  # nosec
