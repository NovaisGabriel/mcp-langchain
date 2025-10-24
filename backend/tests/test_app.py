import json
import pytest
from app import create_app
import chains

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_analyze_success(monkeypatch, client):
    # Mock run_chain to avoid real LLM calls
    def mock_run_chain(text):
        return {"summary": "Mock summary", "sentiment": "Positive", "keywords": ["a","b","c"]}

    monkeypatch.setattr(chains, "run_chain", mock_run_chain)

    response = client.post("/api/analyze", json={"text": "Test text"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["summary"] == "Mock summary"
    assert data["sentiment"] == "Positive"
    assert data["keywords"] == ["a","b","c"]
