"""Unit tests for Python client SDK."""

import pytest
from unittest.mock import MagicMock, patch
from src.client.sdk import SimilarityStudioClient


def test_client_init():
    client = SimilarityStudioClient(base_url="http://localhost:5000")
    assert client.base_url == "http://localhost:5000"


@patch("requests.Session.get")
def test_client_get_stats(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"status": "healthy", "model": "all-MiniLM-L6-v2"}
    mock_resp.raise_for_status = MagicMock()
    mock_get.return_value = mock_resp

    client = SimilarityStudioClient()
    stats = client.get_stats()
    assert stats["status"] == "healthy"
    assert stats["model"] == "all-MiniLM-L6-v2"


@patch("requests.Session.post")
def test_client_compare(mock_post):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        "cosine_similarity": 0.88,
        "percentage": 88.0,
        "tier": "Extremely High Similarity",
    }
    mock_resp.raise_for_status = MagicMock()
    mock_post.return_value = mock_resp

    client = SimilarityStudioClient()
    res = client.compare("hello world", "hi world")
    assert res["percentage"] == 88.0
    assert "Extremely High" in res["tier"]
