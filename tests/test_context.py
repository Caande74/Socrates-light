import pytest
from fastapi.testclient import TestClient

from app.auth.owners import CALLE_OWNER_ID, CALLE_OWNER_NAME
from app.config import settings
from app.db.models.feedback import Feedback
from app.db.session import SessionLocal
from app.main import app
from scripts.migrate_runtime_owners import main as migrate_runtime_owners


API_HEADERS = {"x-api-key": settings.api_key}
CALLE_AUTH_HEADERS = {**API_HEADERS, "x-authenticated-subject": "subject-calle"}
OWNER_A_ID = "11111111-1111-1111-1111-111111111111"
OWNER_B_ID = "22222222-2222-2222-2222-222222222222"
RETRIEVAL_OWNER_ID = "33333333-3333-3333-3333-333333333333"
BETA_OWNER_ID = "44444444-4444-4444-4444-444444444444"
OTHER_OWNER_ID = "55555555-5555-5555-5555-555555555555"


def _client() -> TestClient:
    return TestClient(app)


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/feedback", {"content": "battery risk feedback"}),
        ("/adjustments", {"content": "battery risk adjustment"}),
        ("/patterns", {"content": "battery risk pattern"}),
        ("/assumptions", {"content": "battery risk assumption"}),
        ("/initiatives", {"content": "battery risk initiative"}),
    ],
)
def test_owner_id_is_required_on_context_and_scoped_write_endpoints(path: str, payload: dict):
    client = _client()

    response = client.post(path, headers=API_HEADERS, json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "owner_id or authenticated_subject is required"


def test_context_and_writes_are_fully_isolated_by_owner_id():
    client = _client()
    owner_a = OWNER_A_ID
    owner_b = OWNER_B_ID

    feedback_a = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": owner_a,
            "content": "battery risk feedback shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )
    feedback_b = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": owner_b,
            "content": "battery risk feedback shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )

    adjustment_a = client.post(
        "/adjustments",
        headers=API_HEADERS,
        json={
            "owner_id": owner_a,
            "content": "battery risk adjustment shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )
    adjustment_b = client.post(
        "/adjustments",
        headers=API_HEADERS,
        json={
            "owner_id": owner_b,
            "content": "battery risk adjustment shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )

    pattern_a = client.post(
        "/patterns",
        headers=API_HEADERS,
        json={
            "owner_id": owner_a,
            "content": "battery risk pattern shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )
    pattern_b = client.post(
        "/patterns",
        headers=API_HEADERS,
        json={
            "owner_id": owner_b,
            "content": "battery risk pattern shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )

    assumption_a = client.post(
        "/assumptions",
        headers=API_HEADERS,
        json={
            "owner_id": owner_a,
            "content": "battery risk assumption shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )
    assumption_b = client.post(
        "/assumptions",
        headers=API_HEADERS,
        json={
            "owner_id": owner_b,
            "content": "battery risk assumption shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )

    initiative_a = client.post(
        "/initiatives",
        headers=API_HEADERS,
        json={
            "owner_id": owner_a,
            "content": "battery risk initiative shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )
    initiative_b = client.post(
        "/initiatives",
        headers=API_HEADERS,
        json={
            "owner_id": owner_b,
            "content": "battery risk initiative shared phrase",
            "tags": ["battery", "risk", "shared"],
        },
    )

    for response in [
        feedback_a,
        feedback_b,
        adjustment_a,
        adjustment_b,
        pattern_a,
        pattern_b,
        assumption_a,
        assumption_b,
        initiative_a,
        initiative_b,
    ]:
        assert response.status_code == 200

    assert feedback_a.json()["owner_id"] == owner_a
    assert feedback_b.json()["owner_id"] == owner_b
    assert feedback_a.json()["id"] != feedback_b.json()["id"]

    context_a = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={"query": "battery risk shared phrase", "owner_id": owner_a},
    )
    context_b = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={"query": "battery risk shared phrase", "owner_id": owner_b},
    )

    assert context_a.status_code == 200
    assert context_b.status_code == 200

    payload_a = context_a.json()
    payload_b = context_b.json()

    def ids(payload: dict, key: str) -> set[str]:
        return {item["id"] for item in payload[key]}

    expected_a = {
        "feedback": {feedback_a.json()["id"]},
        "adjustments": {adjustment_a.json()["id"]},
        "patterns": {pattern_a.json()["id"]},
        "assumptions": {assumption_a.json()["id"]},
        "initiatives": {initiative_a.json()["id"]},
    }
    expected_b = {
        "feedback": {feedback_b.json()["id"]},
        "adjustments": {adjustment_b.json()["id"]},
        "patterns": {pattern_b.json()["id"]},
        "assumptions": {assumption_b.json()["id"]},
        "initiatives": {initiative_b.json()["id"]},
    }

    for key, expected_ids in expected_a.items():
        assert ids(payload_a, key) == expected_ids
        assert all(item["owner_id"] == owner_a for item in payload_a[key])
        assert ids(payload_a, key).isdisjoint(expected_b[key])

    for key, expected_ids in expected_b.items():
        assert ids(payload_b, key) == expected_ids
        assert all(item["owner_id"] == owner_b for item in payload_b[key])
        assert ids(payload_b, key).isdisjoint(expected_a[key])

    assert ids(payload_a["guidance"], "adjustments") == expected_a["adjustments"]
    assert ids(payload_a["guidance"], "patterns") == expected_a["patterns"]
    assert ids(payload_b["guidance"], "adjustments") == expected_b["adjustments"]
    assert ids(payload_b["guidance"], "patterns") == expected_b["patterns"]


def test_context_get_supports_explicit_owner_id_without_authenticated_subject():
    client = _client()
    stored_text = "explicit owner context lookup"

    write_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": OWNER_A_ID,
            "content": stored_text,
        },
    )
    assert write_response.status_code == 200

    response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": stored_text,
            "owner_id": OWNER_A_ID,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert response.status_code == 200
    assert response.json()["feedback"]
    assert response.json()["feedback"][0]["id"] == write_response.json()["id"]


def test_context_get_supports_authenticated_subject_without_owner_id_in_body():
    client = _client()
    stored_text = "authenticated subject context lookup"

    write_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": CALLE_OWNER_ID,
            "content": stored_text,
        },
    )
    assert write_response.status_code == 200

    response = client.post(
        "/context/get",
        headers=CALLE_AUTH_HEADERS,
        json={
            "query": stored_text,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert response.status_code == 200
    assert response.json()["feedback"]
    assert response.json()["feedback"][0]["id"] == write_response.json()["id"]


def test_server_side_authenticated_subject_is_attached_from_api_key_config(monkeypatch):
    client = _client()
    stored_text = "server side attached subject lookup"
    monkeypatch.setattr(settings, "api_authenticated_subject", "subject-calle")

    write_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": CALLE_OWNER_ID,
            "content": stored_text,
        },
    )
    assert write_response.status_code == 200

    response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": stored_text,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert response.status_code == 200
    assert response.json()["feedback"]
    assert response.json()["feedback"][0]["id"] == write_response.json()["id"]


def test_server_side_authenticated_subject_has_priority_over_temporary_header_bridge(monkeypatch):
    client = _client()
    stored_text = "server side subject wins over header"
    monkeypatch.setattr(settings, "api_authenticated_subject", "subject-calle")

    write_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": CALLE_OWNER_ID,
            "content": stored_text,
        },
    )
    assert write_response.status_code == 200

    response = client.post(
        "/context/get",
        headers={**API_HEADERS, "x-authenticated-subject": "unmapped-subject"},
        json={
            "query": stored_text,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert response.status_code == 200
    assert response.json()["feedback"]
    assert response.json()["feedback"][0]["id"] == write_response.json()["id"]


def test_server_side_authenticated_subject_is_attached_from_trusted_upstream_header(monkeypatch):
    client = _client()
    stored_text = "trusted upstream subject lookup"
    monkeypatch.setattr(settings, "trusted_authenticated_subject_header", "x-upstream-subject")

    write_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": CALLE_OWNER_ID,
            "content": stored_text,
        },
    )
    assert write_response.status_code == 200

    response = client.post(
        "/context/get",
        headers={**API_HEADERS, "x-upstream-subject": "subject-calle"},
        json={
            "query": stored_text,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert response.status_code == 200
    assert response.json()["feedback"]
    assert response.json()["feedback"][0]["id"] == write_response.json()["id"]


def test_trusted_upstream_subject_has_priority_over_api_fallback(monkeypatch):
    client = _client()
    stored_text = "trusted upstream subject wins over api fallback"

    write_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": CALLE_OWNER_ID,
            "content": stored_text,
        },
    )
    assert write_response.status_code == 200

    monkeypatch.setattr(settings, "trusted_authenticated_subject_header", "x-upstream-subject")
    monkeypatch.setattr(settings, "api_authenticated_subject", "unmapped-subject")

    response = client.post(
        "/context/get",
        headers={**API_HEADERS, "x-upstream-subject": "subject-calle"},
        json={
            "query": stored_text,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert response.status_code == 200
    assert response.json()["feedback"]
    assert response.json()["feedback"][0]["id"] == write_response.json()["id"]


def test_context_get_returns_403_on_authenticated_subject_owner_mismatch():
    client = _client()

    response = client.post(
        "/context/get",
        headers=CALLE_AUTH_HEADERS,
        json={
            "query": "mismatch test",
            "owner_id": OWNER_A_ID,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "authenticated_subject does not match owner_id"


def test_context_get_returns_clear_error_when_owner_is_missing_everywhere():
    client = _client()

    response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": "missing owner context",
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "owner_id or authenticated_subject is required"


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/feedback", {"content": "write explicit owner feedback"}),
        ("/adjustments", {"content": "write explicit owner adjustment"}),
        ("/patterns", {"content": "write explicit owner pattern"}),
        ("/assumptions", {"content": "write explicit owner assumption"}),
        ("/initiatives", {"content": "write explicit owner initiative"}),
    ],
)
def test_write_endpoints_support_explicit_owner_id_without_authenticated_subject(path: str, payload: dict):
    client = _client()

    response = client.post(
        path,
        headers=API_HEADERS,
        json={
            **payload,
            "owner_id": OWNER_A_ID,
        },
    )

    assert response.status_code == 200
    assert response.json()["owner_id"] == OWNER_A_ID


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/feedback", {"content": "write subject feedback"}),
        ("/adjustments", {"content": "write subject adjustment"}),
        ("/patterns", {"content": "write subject pattern"}),
        ("/assumptions", {"content": "write subject assumption"}),
        ("/initiatives", {"content": "write subject initiative"}),
    ],
)
def test_write_endpoints_support_authenticated_subject_without_owner_id(path: str, payload: dict):
    client = _client()

    response = client.post(
        path,
        headers=CALLE_AUTH_HEADERS,
        json=payload,
    )

    assert response.status_code == 200
    assert response.json()["owner_id"] == CALLE_OWNER_ID
    assert response.json()["owner_name"] == CALLE_OWNER_NAME


@pytest.mark.parametrize("path", ["/feedback", "/adjustments", "/patterns", "/assumptions", "/initiatives"])
def test_write_endpoints_return_403_on_authenticated_subject_owner_mismatch(path: str):
    client = _client()

    response = client.post(
        path,
        headers=CALLE_AUTH_HEADERS,
        json={
            "content": "mismatch write",
            "owner_id": OWNER_A_ID,
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "authenticated_subject does not match owner_id"


@pytest.mark.parametrize("path", ["/feedback", "/adjustments", "/patterns", "/assumptions", "/initiatives"])
def test_write_endpoints_return_clear_error_when_owner_is_missing_everywhere(path: str):
    client = _client()

    response = client.post(
        path,
        headers=API_HEADERS,
        json={
            "content": "missing owner write",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "owner_id or authenticated_subject is required"


def test_feedback_write_accepts_missing_tags():
    client = _client()
    stored_text = "TEST tags fri skrivning 11"

    response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": CALLE_OWNER_ID,
            "content": stored_text,
        },
    )

    assert response.status_code == 200
    assert response.json()["tags"] is None
    assert response.json()["owner_name"] == CALLE_OWNER_NAME
    assert response.json()["legacy_owner"] is None

    retrieval_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": stored_text,
            "owner_id": CALLE_OWNER_ID,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert retrieval_response.status_code == 200
    assert retrieval_response.json()["feedback"]
    assert retrieval_response.json()["feedback"][0]["id"] == response.json()["id"]


def test_feedback_retrieval_prefers_exact_and_near_match_within_owner_scope():
    client = _client()
    owner_id = RETRIEVAL_OWNER_ID
    stored_text = "TEST retrieval robust 44"

    write_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": owner_id,
            "content": stored_text,
            "title": stored_text,
        },
    )

    assert write_response.status_code == 200
    feedback_id = write_response.json()["id"]

    exact_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": stored_text,
            "owner_id": owner_id,
            "mode": "analysis",
            "role": "operator",
        },
    )

    near_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": "kan du hamta feedback om retrieval robust 44",
            "owner_id": owner_id,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert exact_response.status_code == 200
    assert near_response.status_code == 200

    exact_feedback = exact_response.json()["feedback"]
    near_feedback = near_response.json()["feedback"]

    assert exact_feedback
    assert near_feedback
    assert exact_feedback[0]["id"] == feedback_id
    assert near_feedback[0]["id"] == feedback_id
    assert exact_feedback[0]["retrieval_path"] == "direct"
    assert near_feedback[0]["retrieval_path"] == "direct"


def test_feedback_retrieval_does_not_return_weak_generic_false_positive():
    client = _client()

    beta_write = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": BETA_OWNER_ID,
            "content": "TEST beta isolering 73",
            "title": "TEST beta isolering 73",
        },
    )
    alfa_write = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": OTHER_OWNER_ID,
            "content": "TEST alfa isolering 22",
            "title": "TEST alfa isolering 22",
        },
    )

    assert beta_write.status_code == 200
    assert alfa_write.status_code == 200

    beta_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": "TEST beta isolering 73",
            "owner_id": BETA_OWNER_ID,
            "mode": "analysis",
            "role": "operator",
        },
    )
    alfa_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": "TEST beta isolering 73",
            "owner_id": OTHER_OWNER_ID,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert beta_response.status_code == 200
    assert alfa_response.status_code == 200
    assert beta_response.json()["feedback"]
    assert beta_response.json()["feedback"][0]["id"] == beta_write.json()["id"]
    assert alfa_response.json()["feedback"] == []


def test_context_retrieves_needs_review_but_not_inactive_feedback():
    client = _client()
    owner_id = OWNER_A_ID

    active_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": owner_id,
            "content": "status lifecycle active feedback",
            "title": "status lifecycle active feedback",
            "status": "active",
        },
    )
    review_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": owner_id,
            "content": "status lifecycle review feedback",
            "title": "status lifecycle review feedback",
            "status": "needs_review",
        },
    )
    inactive_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": owner_id,
            "content": "status lifecycle inactive feedback",
            "title": "status lifecycle inactive feedback",
            "status": "inactive",
        },
    )

    assert active_response.status_code == 200
    assert review_response.status_code == 200
    assert inactive_response.status_code == 200

    context_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={
            "query": "status lifecycle feedback",
            "owner_id": owner_id,
            "mode": "analysis",
            "role": "operator",
        },
    )

    assert context_response.status_code == 200
    feedback_items = context_response.json()["feedback"]
    feedback_ids = {item["id"] for item in feedback_items}

    assert active_response.json()["id"] in feedback_ids
    assert review_response.json()["id"] in feedback_ids
    assert inactive_response.json()["id"] not in feedback_ids


def test_context_ranks_active_feedback_ahead_of_equivalent_needs_review_item():
    client = _client()
    owner_id = OWNER_B_ID
    query = "equivalent feedback ranking token"

    active_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": owner_id,
            "content": query,
            "title": query,
            "status": "active",
        },
    )
    review_response = client.post(
        "/feedback",
        headers=API_HEADERS,
        json={
            "owner_id": owner_id,
            "content": f"{query} review variant",
            "title": query,
            "status": "needs_review",
        },
    )

    assert active_response.status_code == 200
    assert review_response.status_code == 200

    context_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={"query": query, "owner_id": owner_id},
    )

    assert context_response.status_code == 200
    feedback_items = context_response.json()["feedback"]

    assert len(feedback_items) >= 2
    assert feedback_items[0]["id"] == active_response.json()["id"]
    assert feedback_items[1]["id"] == review_response.json()["id"]


def test_context_excludes_invalid_assumptions():
    client = _client()
    owner_id = RETRIEVAL_OWNER_ID
    query = "falsified lifecycle assumption"

    valid_response = client.post(
        "/assumptions",
        headers=API_HEADERS,
        json={
            "owner_id": owner_id,
            "content": query,
            "title": query,
            "status": "active",
        },
    )
    invalid_response = client.post(
        "/assumptions",
        headers=API_HEADERS,
        json={
            "owner_id": owner_id,
            "content": query,
            "title": query,
            "status": "invalid",
        },
    )

    assert valid_response.status_code == 200
    assert invalid_response.status_code == 200

    context_response = client.post(
        "/context/get",
        headers=API_HEADERS,
        json={"query": query, "owner_id": owner_id},
    )

    assert context_response.status_code == 200
    assumption_ids = {item["id"] for item in context_response.json()["assumptions"]}

    assert valid_response.json()["id"] in assumption_ids
    assert invalid_response.json()["id"] not in assumption_ids


def test_runtime_owner_migration_moves_only_known_legacy_identity_rows():
    with SessionLocal() as db:
        db.add(
            Feedback(
                id="feedback-legacy-calle",
                title="Legacy Calle",
                content="legacy calle post",
                status="active",
                owner_id="calle",
            )
        )
        db.add(
            Feedback(
                id="feedback-legacy-alfa",
                title="Legacy Alfa",
                content="legacy alfa 22 post",
                status="active",
                owner_id="alfa 22",
            )
        )
        db.add(
            Feedback(
                id="feedback-legacy-unsafe",
                title="Legacy Unsafe",
                content="legacy unknown owner post",
                status="active",
                owner_id="beta 73",
            )
        )
        db.commit()

    migrate_runtime_owners()

    with SessionLocal() as db:
        migrated_calle = db.get(Feedback, "feedback-legacy-calle")
        migrated_alfa = db.get(Feedback, "feedback-legacy-alfa")
        untouched_unknown = db.get(Feedback, "feedback-legacy-unsafe")

    assert migrated_calle.owner_id == CALLE_OWNER_ID
    assert migrated_calle.owner_name == CALLE_OWNER_NAME
    assert migrated_calle.legacy_owner == "calle"

    assert migrated_alfa.owner_id == CALLE_OWNER_ID
    assert migrated_alfa.owner_name == CALLE_OWNER_NAME
    assert migrated_alfa.legacy_owner == "alfa 22"

    assert untouched_unknown.owner_id == "beta 73"
    assert untouched_unknown.owner_name is None
    assert untouched_unknown.legacy_owner is None
