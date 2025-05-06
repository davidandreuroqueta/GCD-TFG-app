import pytest
from api.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()

def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.data == b"ok"

def test_quote_endpoint(client):
    resp = client.get("/v1/quote")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "total" in data
    assert isinstance(data["lines"], list)
    assert data["lines"][0]["item"] == "Pieza A"
