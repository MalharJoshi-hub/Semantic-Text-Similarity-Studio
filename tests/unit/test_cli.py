"""Unit tests for CLI parser."""

import pytest
import sys
from unittest.mock import patch
from src.client.cli import main


def test_cli_help(capsys):
    with pytest.raises(SystemExit) as exc:
        with patch.object(sys, "argv", ["similarity-studio", "--help"]):
            main()
    assert exc.value.code == 0
    captured = capsys.readouterr()
    assert "Semantic Text Similarity" in captured.out


def test_cli_compare(capsys):
    with patch("src.client.sdk.SimilarityStudioClient.compare") as mock_comp:
        mock_comp.return_value = {
            "percentage": 92.5,
            "tier": "Extremely High Similarity",
            "cosine_similarity": 0.925,
            "lexical_overlap": 0.65,
        }
        with patch.object(sys, "argv", ["similarity-studio", "compare", "--t1", "dog", "--t2", "canine"]):
            main()
        captured = capsys.readouterr()
        assert "Similarity: 92.5%" in captured.out
