"""Integration tests for Flask HTTP endpoints."""

import pytest


def test_endpoint_health(flask_test_client):
    res = flask_test_client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"


def test_endpoint_stats(flask_test_client):
    res = flask_test_client.get("/api/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert "model" in data
    assert "corpus" in data
    assert "engine" in data


def test_endpoint_similarity_pair_success(flask_test_client):
    payload = {
        "text1": "The quick brown fox jumped over the lazy dog.",
        "text2": "A fast auburn fox bounded across the sleeping canine."
    }
    res = flask_test_client.post("/api/similarity/pair", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert "cosine_similarity" in data
    assert data["cosine_similarity"] > 0.60
    assert "percentage" in data
    assert "tier" in data


def test_endpoint_similarity_pair_validation_error(flask_test_client):
    res = flask_test_client.post("/api/similarity/pair", json={"text1": ""})
    assert res.status_code == 400


def test_endpoint_texts_list(flask_test_client):
    res = flask_test_client.get("/api/texts")
    assert res.status_code == 200
    data = res.get_json()
    assert "texts" in data
    assert "total" in data
