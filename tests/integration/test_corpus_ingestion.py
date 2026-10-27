"""Integration tests for document corpus ingestion and FAISS synchronization."""

import pytest


def test_corpus_ingest_and_search_flow(flask_test_client):
    # 1. Ingest new document
    doc_payload = {
        "label": "Architecture Guide",
        "content": """# System Architecture
The architecture comprises five discrete layers: API, Embeddings, FAISS Index, Storage, and Tests.
Each layer maintains strict encapsulation and clean interfaces.
"""
    }
    resp = flask_test_client.post("/api/texts", json=doc_payload)
    assert resp.status_code == 201
    doc_data = resp.get_json()
    doc_id = doc_data["document"]["id"]
    assert doc_id is not None

    # 2. Search corpus for relevant query
    search_payload = {
        "query": "five architectural layers and interfaces",
        "top_k": 3
    }
    s_resp = flask_test_client.post("/api/similarity/query", json=search_payload)
    assert s_resp.status_code == 200
    s_data = s_resp.get_json()
    assert s_data["total_matches"] > 0
    top_match = s_data["results"][0]
    assert "Architecture" in top_match["doc_label"]
    assert top_match["score"] > 0.50

    # 3. Clean up by deleting document
    del_resp = flask_test_client.delete(f"/api/texts/{doc_id}")
    assert del_resp.status_code == 200
