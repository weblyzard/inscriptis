import pytest
from fastapi.testclient import TestClient

from inscriptis.metadata import __version__
from inscriptis.service.web import app


@pytest.fixture
def client():
    return TestClient(app)


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Inscriptis text to HTML Web service."


def test_get_text_call_with_content_type(client):
    html_content = "<html><body>Österliche Freuden!</body></html>"
    response = client.post(
        "/get_text",
        content=html_content,
        headers={"Content-type": "text/html; charset=UTF-8"},
    )
    assert response.status_code == 200
    assert response.text == "Österliche Freuden!"


def test_get_text_call_without_content_type(client):
    html_content = "<html><body>Hello World!</body></html>"
    response = client.post(
        "/get_text",
        content=html_content,
        headers={"Content-type": "text/html"},
    )
    assert response.status_code == 200
    assert response.text == "Hello World!"


def test_get_version_call(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert response.text == __version__
