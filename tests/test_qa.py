"""Tests for /qa endpoint (fallback path)."""

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from fastapi.testclient import TestClient  # after path tweak

from app.main import app

client = TestClient(app)


def test_qa_mock() -> None:
    """Test QA endpoint with mocked OpenAI response."""
    # Test with minimal valid input
    resp = client.post("/api/v1/qa", json={
        "text": "## Zugspitze\nDie Zugspitze ist der höchste Berg Deutschlands mit 2962 Metern Höhe.",
        "num_pairs": 3
    })
    assert resp.status_code == 200
    assert len(resp.json()["qa"]) >= 1
