"""Statistical evaluation, correlation, and ranking metrics."""

from typing import List, Sequence, Tuple
import numpy as np


def compute_pearson_correlation(preds: Sequence[float], targets: Sequence[float]) -> float:
    """Compute Pearson correlation coefficient r between predictions and targets."""
    p = np.asarray(preds, dtype=np.float64)
    t = np.asarray(targets, dtype=np.float64)
    if len(p) != len(t) or len(p) < 2:
        return 0.0
    diff_p = p - np.mean(p)
    diff_t = t - np.mean(t)
    denom = np.sqrt(np.sum(diff_p ** 2) * np.sum(diff_t ** 2))
    if denom == 0.0:
        return 0.0
    return float(np.sum(diff_p * diff_t) / denom)


def compute_spearman_correlation(preds: Sequence[float], targets: Sequence[float]) -> float:
    """Compute Spearman rank-order correlation coefficient rho."""
    p = np.asarray(preds, dtype=np.float64)
    t = np.asarray(targets, dtype=np.float64)
    if len(p) != len(t) or len(p) < 2:
        return 0.0

    def _rank(arr: np.ndarray) -> np.ndarray:
        temp = arr.argsort()
        ranks = np.empty_like(temp, dtype=np.float64)
        ranks[temp] = np.arange(len(arr), dtype=np.float64)
        return ranks

    rank_p = _rank(p)
    rank_t = _rank(t)
    return compute_pearson_correlation(rank_p, rank_t)


def compute_precision_recall_at_k(retrieved_ids: Sequence[int], relevant_ids: Sequence[int], k: int = 5) -> Tuple[float, float]:
    """Compute Precision@K and Recall@K for information retrieval evaluation."""
    if k <= 0:
        return 0.0, 0.0
    top_k = retrieved_ids[:k]
    rel_set = set(relevant_ids)
    if not rel_set:
        return 0.0, 0.0

    hits = sum(1 for item in top_k if item in rel_set)
    precision = hits / float(k)
    recall = hits / float(len(rel_set))
    return precision, recall


def compute_ndcg_at_k(retrieved_ids: Sequence[int], relevant_ids: Sequence[int], k: int = 5) -> float:
    """Compute Normalized Discounted Cumulative Gain (NDCG@K) with binary relevance."""
    if k <= 0 or not relevant_ids:
        return 0.0
    top_k = retrieved_ids[:k]
    rel_set = set(relevant_ids)

    dcg = 0.0
    for idx, item in enumerate(top_k):
        if item in rel_set:
            dcg += 1.0 / np.log2(idx + 2)

    idcg = 0.0
    ideal_hits = min(k, len(rel_set))
    for idx in range(ideal_hits):
        idcg += 1.0 / np.log2(idx + 2)

    return float(dcg / idcg) if idcg > 0.0 else 0.0
