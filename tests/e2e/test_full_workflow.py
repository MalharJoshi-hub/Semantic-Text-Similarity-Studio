"""End-to-End simulation testing complete user journeys."""

import pytest


def test_full_user_workflow(flask_test_client):
    # Step 1: Healthcheck
    health_resp = flask_test_client.get("/health")
    assert health_resp.status_code == 200

    # Step 2: Pairwise comparison
    sim_resp = flask_test_client.post("/api/similarity/pair", json={
        "text1": "The quick brown fox jumps over the lazy dog.",
        "text2": "A quick brown fox leaps across a sleeping dog."
    })
    assert sim_resp.status_code == 200
    assert sim_resp.get_json()["cosine_similarity"] > 0.75

    # Step 3: Seed domain pack
    seed_resp = flask_test_client.post("/api/datasets/seed", json={"domain": "legal"})
    assert seed_resp.status_code == 200
    seed_data = seed_resp.get_json()
    assert seed_data["status"] == "success"

    # Step 4: Search corpus
    query_resp = flask_test_client.post("/api/similarity/query", json={
        "query": "liability indemnification breach of contract",
        "top_k": 3
    })
    assert query_resp.status_code == 200
    results = query_resp.get_json()["results"]
    assert len(results) > 0
