from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


API_HEADERS = {"x-api-key": settings.api_key}
OWNER_ID = "11111111-1111-1111-1111-111111111111"


def _client() -> TestClient:
    return TestClient(app)


def test_assumption_create_accepts_invalid_status():
    client = _client()

    response = client.post(
        "/assumptions",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "assumption with invalid lifecycle status",
            "status": "invalid",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "invalid"


def test_assumption_status_patch_updates_status_and_hides_invalid_from_context():
    client = _client()

    create_response = client.post(
        "/assumptions",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "assumption patch lifecycle test",
            "title": "assumption patch lifecycle test",
            "status": "active",
        },
    )

    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/assumptions/{item_id}/status",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "status": "invalid",
        },
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "invalid"

    context_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={"query": "assumption patch lifecycle test", "owner_id": OWNER_ID},
    )

    assert context_response.status_code == 200
    assumption_ids = {item["id"] for item in context_response.json()["assumptions"]}
    assert item_id not in assumption_ids


def test_assumption_status_patch_enforces_owner_scope():
    client = _client()

    create_response = client.post(
        "/assumptions",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "assumption owner scoped patch test",
            "status": "active",
        },
    )
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/assumptions/{item_id}/status",
        headers=API_HEADERS,
        json={
            "owner_id": "22222222-2222-2222-2222-222222222222",
            "status": "needs_review",
        },
    )

    assert patch_response.status_code == 404
