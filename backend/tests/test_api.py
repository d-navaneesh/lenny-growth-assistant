from __future__ import annotations


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ready(client):
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] in {"ok", "degraded"}


def test_sessions_round_trip(client):
    created = client.post("/api/v1/sessions", json={"title": "Demo session", "owner": "tester"})
    assert created.status_code == 200
    session_id = created.json()["id"]
    listing = client.get("/api/v1/sessions")
    assert listing.status_code == 200
    assert any(item["id"] == session_id for item in listing.json()["items"])

    messages = client.get(f"/api/v1/sessions/{session_id}/messages")
    assert messages.status_code == 200


def test_invalid_model_selection(client):
    response = client.post("/api/v1/models/select", json={"provider": "fake", "model": "n/a"})
    assert response.status_code == 422


def test_chat_response(client):
    session = client.post("/api/v1/sessions", json={"title": "Chat session"})
    session_id = session.json()["id"]
    resp = client.post("/api/v1/chat", json={"session_id": session_id, "prompt": "How should a startup find product-market fit?"})
    assert resp.status_code == 200
    body = resp.json()
    assert "response" in body
    assert body["provider"] in {"ollama", "openai", "anthropic"}
