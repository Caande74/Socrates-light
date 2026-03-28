from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


API_HEADERS = {"x-api-key": settings.api_key}
OWNER_ID = "11111111-1111-1111-1111-111111111111"


def _client() -> TestClient:
    return TestClient(app)


def test_initiatives_active_endpoint_remains_strict_active():
    client = _client()

    active_response = client.post(
        "/initiatives",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "strict active initiative",
            "status": "active",
        },
    )
    review_response = client.post(
        "/initiatives",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "needs review initiative",
            "status": "needs_review",
        },
    )

    assert active_response.status_code == 200
    assert review_response.status_code == 200

    list_response = client.get("/initiatives/active", headers=API_HEADERS)

    assert list_response.status_code == 200
    returned_ids = {item["id"] for item in list_response.json()}
    assert active_response.json()["id"] in returned_ids
    assert review_response.json()["id"] not in returned_ids


def test_initiative_status_patch_updates_context_and_strict_active_endpoint():
    client = _client()

    create_response = client.post(
        "/initiatives",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "initiative patch lifecycle test",
            "title": "initiative patch lifecycle test",
            "status": "active",
        },
    )

    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/initiatives/{item_id}/status",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "status": "needs_review",
        },
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["status"] == "needs_review"

    context_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={"query": "initiative patch lifecycle test", "owner_id": OWNER_ID},
    )
    list_response = client.get("/initiatives/active", headers=API_HEADERS)

    assert context_response.status_code == 200
    assert list_response.status_code == 200

    context_ids = {item["id"] for item in context_response.json()["initiatives"]}
    active_ids = {item["id"] for item in list_response.json()}

    assert item_id in context_ids
    assert item_id not in active_ids


def test_initiative_status_patch_rejects_invalid_status():
    client = _client()

    create_response = client.post(
        "/initiatives",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "initiative invalid patch test",
            "status": "active",
        },
    )

    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/initiatives/{item_id}/status",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "status": "invalid",
        },
    )

    assert patch_response.status_code == 422


def test_initiative_status_patch_enforces_owner_scope():
    client = _client()

    create_response = client.post(
        "/initiatives",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_ID,
            "content": "initiative owner scoped patch test",
            "status": "active",
        },
    )

    assert create_response.status_code == 200
    item_id = create_response.json()["id"]

    patch_response = client.patch(
        f"/initiatives/{item_id}/status",
        headers=API_HEADERS,
        json={
            "owner_id": "22222222-2222-2222-2222-222222222222",
            "status": "inactive",
        },
    )

    assert patch_response.status_code == 404
