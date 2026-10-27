"""Unit tests for statistical correlation and ranking metrics."""

import pytest
import numpy as np
from src.core.metrics import (
    compute_pearson_correlation,
    compute_spearman_correlation,
    compute_precision_recall_at_k,
    compute_ndcg_at_k,
)


def test_pearson_correlation():
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [2.0, 4.0, 6.0, 8.0, 10.0]
    r = compute_pearson_correlation(x, y)
    assert np.isclose(r, 1.0, atol=1e-5)

    neg_y = [10.0, 8.0, 6.0, 4.0, 2.0]
    r_neg = compute_pearson_correlation(x, neg_y)
    assert np.isclose(r_neg, -1.0, atol=1e-5)


def test_spearman_correlation():
    x = [1, 2, 3, 4, 5]
    y = [10, 20, 30, 40, 50]
    rho = compute_spearman_correlation(x, y)
    assert np.isclose(rho, 1.0, atol=1e-5)


def test_precision_recall_at_k():
    retrieved = [1, 2, 3, 4, 5]
    relevant = [2, 4, 6, 8]

    # At k=5: hits = {2, 4} (2 hits)
    # Precision@5 = 2/5 = 0.4
    # Recall@5 = 2/4 = 0.5
    p, r = compute_precision_recall_at_k(retrieved, relevant, k=5)
    assert np.isclose(p, 0.4)
    assert np.isclose(r, 0.5)


def test_ndcg_at_k():
    retrieved = [1, 2, 3, 4]
    relevant = [1, 2]

    # Perfect ranking at top 2
    ndcg = compute_ndcg_at_k(retrieved, relevant, k=4)
    assert np.isclose(ndcg, 1.0, atol=1e-5)

    # Suboptimal ranking
    bad_retrieved = [3, 4, 1, 2]
    bad_ndcg = compute_ndcg_at_k(bad_retrieved, relevant, k=4)
    assert bad_ndcg < 1.0
    assert bad_ndcg > 0.0
