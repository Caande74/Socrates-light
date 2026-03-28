from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


API_HEADERS = {"x-api-key": settings.api_key}
OWNER_ID = "11111111-1111-1111-1111-111111111111"


def _client() -> TestClient:
    return TestClient(app)


def test_feedback_create_rejects_invalid_status():
    client = _client()

    response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "feedback with invalid lifecycle status",
            "status": "invalid",
        },
    )

    assert response.status_code == 422
    assert "status must be one of" in response.text


def test_feedback_status_patch_updates_retrieval_immediately():
    client = _client()

    create_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "feedback patch lifecycle test",
            "title": "feedback patch lifecycle test",
            "status": "active",
        },
    )

    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/feedback/{item_id}/status",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "status": "inactive",
        },
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "inactive"

    context_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={"query": "feedback patch lifecycle test", "owner_id": OWNER_ID},
    )

    assert context_response.status_code == 200
    feedback_ids = {item["id"] for item in context_response.json()["feedback"]}
    assert item_id not in feedback_ids


def test_feedback_status_patch_rejects_invalid_status():
    client = _client()

    create_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "feedback invalid patch test",
            "status": "active",
        },
    )

    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/feedback/{item_id}/status",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "status": "invalid",
        },
    )

    assert patch_response.status_code == 422


def test_feedback_status_patch_enforces_owner_scope():
    client = _client()

    create_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "feedback owner scoped patch test",
            "status": "active",
        },
    )

    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/feedback/{item_id}/status",
        headers=API_HEADERS,
        json={
            "owner_id": "22222222-2222-2222-2222-222222222222",
            "status": "inactive",
        },
    )

    assert patch_response.status_code == 404
