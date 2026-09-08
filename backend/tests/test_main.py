from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat_routes_without_execution() -> None:
    response = client.post(
        "/api/chat",
        json={"mode": "nova", "message": "Check system health"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "nova"
    assert body["executed"] is False
    assert body["provider"] == "core-only"


def test_invalid_chat_mode_is_rejected() -> None:
    response = client.post(
        "/api/chat",
        json={"mode": "unknown", "message": "hello"},
    )
    assert response.status_code == 400


def test_chat_message_length_is_bounded() -> None:
    response = client.post(
        "/api/chat",
        json={"mode": "nova", "message": "x" * 4001},
    )
    assert response.status_code == 422


def test_low_risk_read_only_action_can_be_ready() -> None:
    response = client.post(
        "/api/actions/plan",
        json={
            "action_type": "read_health",
            "description": "Read local service health",
            "risk": "low",
            "external_effect": False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["executed"] is False
    assert body["receipt"]["decision"] == "allow"
    assert body["receipt"]["state"] == "ready"


def test_medium_risk_action_stops_for_policy_review() -> None:
    response = client.post(
        "/api/actions/plan",
        json={
            "action_type": "change_setting",
            "description": "Change a predefined local setting",
            "risk": "medium",
            "external_effect": False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["receipt"]["decision"] == "review"
    assert body["receipt"]["state"] == "waiting_policy"


def test_external_or_high_risk_action_requires_approval() -> None:
    response = client.post(
        "/api/actions/plan",
        json={
            "action_type": "send_message",
            "description": "Send a message to an external recipient",
            "risk": "high",
            "external_effect": True,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["executed"] is False
    assert body["receipt"]["decision"] == "require_approval"
    assert body["receipt"]["state"] == "waiting_approval"
