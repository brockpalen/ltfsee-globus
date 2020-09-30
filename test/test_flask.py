"""Basic flask functioning tests."""
import pytest  # noqa:


def test_flask_install(client):
    """Check that the API page with swagger exists."""
    response = client.get("/api/v0.5/", content_type="html/text")
    assert response.status_code == 200  # nosec
