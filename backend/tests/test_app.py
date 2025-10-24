# tests/test_app.py
import json
import pytest
from app import app, db, Message

@pytest.fixture
def client():
    # Setup: create a test client and temporary DB
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # in-memory DB for tests
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    # Teardown
    with app.app_context():
        db.drop_all()

def test_analyze_endpoint(client, monkeypatch):
    """Test /api/analyze endpoint returns valid JSON keys."""

    # --- Mock the LangChain chain output so we don't call the real API ---
    def fake_run_chain(prompt, text):
        if "Summarize" in prompt.messages[0].prompt.template:
            return "This is a summary."
        elif "sentiment" in prompt.messages[0].prompt.template.lower():
            return "Positive"
        else:
            return "AI, LangChain, Flask"

    monkeypatch.setattr("app.run_chain", fake_run_chain)

    # --- Send test request ---
    response = client.post(
        "/api/analyze",
        data=json.dumps({"text": "I love using AI tools like LangChain!"}),
        content_type="application/json",
    )

    # --- Assertions ---
    assert response.status_code == 200
    data = response.get_json()

    assert "summary" in data
    assert "sentiment" in data
    assert "keywords" in data
    assert data["sentiment"] == "Positive"

    # --- DB check ---
    with app.app_context():
        saved = Message.query.first()
        assert saved is not None
        assert "summary" in saved.summarization.lower()
