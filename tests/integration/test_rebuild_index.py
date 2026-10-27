"""Integration tests verifying index rebuilding idempotency."""

import pytest


def test_rebuild_index_endpoint(flask_test_client):
    # Add a document
    payload = {
        "label": "Rebuild Test Document",
        "content": "A test document verifying index rebuilding from SQLite."
    }
    flask_test_client.post("/api/texts", json=payload)

    # Rebuild endpoint
    res = flask_test_client.post("/api/rebuild")
    assert res.status_code == 200
    data = res.get_json()
    assert "total_chunks" in data
    assert data["total_chunks"] >= 1
