"""Unit tests for vector normalization and score clamping."""

import pytest
import numpy as np
from src.core.normalization import (
    normalize_l2,
    clamp_score,
    cosine_distance_to_similarity,
    l2_distance_to_similarity,
)


def test_normalize_l2_1d():
    vec = np.array([3.0, 4.0], dtype=np.float32)
    normed = normalize_l2(vec)
    assert np.isclose(np.linalg.norm(normed), 1.0, atol=1e-5)
    assert np.isclose(normed[0], 0.6, atol=1e-5)
    assert np.isclose(normed[1], 0.8, atol=1e-5)


def test_normalize_l2_2d():
    vecs = np.array([[1.0, 1.0], [0.0, 5.0]], dtype=np.float32)
    normed = normalize_l2(vecs)
    row_norms = np.linalg.norm(normed, axis=1)
    assert np.allclose(row_norms, [1.0, 1.0], atol=1e-5)


def test_normalize_zero_vector_stability():
    zero_vec = np.zeros(10, dtype=np.float32)
    normed = normalize_l2(zero_vec)
    assert not np.isnan(normed).any()
    assert not np.isinf(normed).any()


def test_clamp_score_bounds():
    assert clamp_score(0.75) == 0.75
    assert clamp_score(1.5) == 1.0
    assert clamp_score(-0.3) == 0.0
    assert clamp_score(0.0) == 0.0
    assert clamp_score(1.0) == 1.0


def test_clamp_score_nan_inf():
    assert clamp_score(float("nan")) == 0.0
    assert clamp_score(float("-inf")) == 0.0
    assert clamp_score(float("inf")) == 1.0


def test_distance_conversions():
    assert np.isclose(cosine_distance_to_similarity(0.2), 0.8)
    assert np.isclose(cosine_distance_to_similarity(1.5), 0.0)
    assert np.isclose(l2_distance_to_similarity(0.0), 1.0)
    assert np.isclose(l2_distance_to_similarity(2.0), 0.0)
