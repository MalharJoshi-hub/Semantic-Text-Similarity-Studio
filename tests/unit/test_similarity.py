"""Unit tests for pairwise similarity metrics and tier classification."""

import pytest
import numpy as np
from src.core.similarity import (
    compute_cosine_similarity,
    compute_lexical_jaccard,
    classify_similarity_tier,
    tokenize_clean,
)


def test_tokenize_clean():
    text = "Hello, world! This is a test 123."
    tokens = tokenize_clean(text)
    assert tokens == ["hello", "world", "this", "is", "a", "test", "123"]


def test_compute_lexical_jaccard():
    t1 = "the quick brown fox"
    t2 = "the fast brown fox"
    # non-stopwords: {quick, brown, fox} vs {fast, brown, fox}
    # intersection: {brown, fox} (2), union: {quick, fast, brown, fox} (4) => 0.5
    jaccard = compute_lexical_jaccard(t1, t2, remove_stopwords=True)
    assert np.isclose(jaccard, 0.5, atol=1e-3)


def test_compute_lexical_jaccard_identical():
    text = "Machine learning vector similarity search."
    jaccard = compute_lexical_jaccard(text, text)
    assert np.isclose(jaccard, 1.0)


def test_compute_lexical_jaccard_disjoint():
    t1 = "aerospace propulsion systems"
    t2 = "culinary recipe ingredients"
    jaccard = compute_lexical_jaccard(t1, t2)
    assert jaccard == 0.0


def test_compute_cosine_similarity():
    v1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    v2 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    v3 = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    v4 = np.array([-1.0, 0.0, 0.0], dtype=np.float32)

    assert np.isclose(compute_cosine_similarity(v1, v2), 1.0)
    assert np.isclose(compute_cosine_similarity(v1, v3), 0.0)
    # Opposite direction is clamped to 0.0
    assert np.isclose(compute_cosine_similarity(v1, v4), 0.0)


def test_classify_similarity_tier():
    name, color, _ = classify_similarity_tier(0.92)
    assert "Extremely High" in name
    assert color == "#10b981"

    name, color, _ = classify_similarity_tier(0.78)
    assert "High Semantic" in name

    name, color, _ = classify_similarity_tier(0.55)
    assert "Moderate" in name

    name, color, _ = classify_similarity_tier(0.38)
    assert "Low" in name

    name, color, _ = classify_similarity_tier(0.12)
    assert "Unrelated" in name
