import pytest
from fastapi.testclient import TestClient
from httpx import RequestError

from app.main import app
from requests.models import Response




@pytest.fixture
def client():
    return TestClient(app)

def mock_502_response(*args, **kwargs):
    mock_response = Response()
    mock_response.status_code = 502
    mock_response._content = b'Bad Gateway'
    return mock_response

def test_check_404_url(client):
    non_existing_category = "hola"
    response = client.get(non_existing_category)
    assert response.status_code == 404

def test_check_200_url(client):
    path = "c/inmuebles"
    response = client.get(path)
    assert response.status_code == 200


def raise_request_error(
        body="",
        client="",
        headers=[],
        params=[],
        request="",
        url=""
):
    raise RequestError("Error calling endpoint")

def test_controller_with_mocked_httpx(monkeypatch: pytest.MonkeyPatch, client):
    monkeypatch.setattr("app.controllers.proxy_controller.call_external_api", raise_request_error)
    response = client.get("/Pinturerias/MLA2302")
    assert response.status_code == 502


