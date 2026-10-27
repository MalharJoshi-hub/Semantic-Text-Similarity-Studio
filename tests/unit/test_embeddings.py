"""Unit tests for EmbeddingEngine and transformer encoding."""

import pytest
import numpy as np
from src.core.embeddings import EmbeddingEngine, get_embedding_engine


def test_embedding_engine_singleton():
    e1 = get_embedding_engine()
    e2 = get_embedding_engine()
    assert e1 is e2
    assert e1.dimension == 384


def test_embedding_encode_single():
    engine = get_embedding_engine()
    vec = engine.encode("Artificial intelligence and natural language processing.")
    assert isinstance(vec, np.ndarray)
    assert vec.ndim == 1
    assert vec.shape[0] == 384
    # Check L2 unit norm
    norm = np.linalg.norm(vec)
    assert np.isclose(norm, 1.0, atol=1e-4)


def test_embedding_encode_batch():
    engine = get_embedding_engine()
    texts = [
        "First document sentence.",
        "Second sentence discussing vector databases.",
        "Third sentence on FAISS indexing."
    ]
    vecs = engine.encode(texts, batch_size=2, normalize=True)
    assert isinstance(vecs, np.ndarray)
    assert vecs.ndim == 2
    assert vecs.shape == (3, 384)
    norms = np.linalg.norm(vecs, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-4)


def test_embedding_encode_empty():
    engine = get_embedding_engine()
    vecs = engine.encode([])
    assert vecs.shape == (0, 384)
