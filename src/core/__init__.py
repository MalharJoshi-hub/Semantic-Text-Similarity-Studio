"""Core NLP and Vector Embedding Package.

This package provides mathematical normalization, pairwise similarity metrics,
and Sentence-Transformer model orchestration.
"""

from src.core.embeddings import EmbeddingEngine, get_embedding_engine
from src.core.normalization import normalize_l2, clamp_score
from src.core.similarity import (
    compute_cosine_similarity,
    compute_lexical_jaccard,
    evaluate_pairwise_similarity,
    classify_similarity_tier,
)
from src.core.types import SimilarityResult, TierInfo

__all__ = [
    "EmbeddingEngine",
    "get_embedding_engine",
    "normalize_l2",
    "clamp_score",
    "compute_cosine_similarity",
    "compute_lexical_jaccard",
    "evaluate_pairwise_similarity",
    "classify_similarity_tier",
    "SimilarityResult",
    "TierInfo",
]
