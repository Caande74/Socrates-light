from app.main import app
from fastapi.testclient import TestClient
from app.config import settings


def test_context_requires_key_and_returns_payload():
    client = TestClient(app)
    response = client.post('/context/get', headers={'x-api-key': settings.api_key}, json={'query': 'test'})
    assert response.status_code == 200
    assert 'notes' in response.json()
