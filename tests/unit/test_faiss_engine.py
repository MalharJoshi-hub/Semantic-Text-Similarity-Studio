"""Unit tests for FaissIndexEngine."""

import pytest
import numpy as np


def test_faiss_engine_init(test_faiss_engine):
    assert test_faiss_engine.dimension == 384
    assert test_faiss_engine.total_vectors == 0


def test_faiss_engine_add_and_search(test_faiss_engine, sample_vectors):
    meta = [{"id": i, "title": f"Doc {i}"} for i in range(len(sample_vectors))]
    assigned_ids = test_faiss_engine.add_vectors(sample_vectors, meta)
    assert len(assigned_ids) == len(sample_vectors)
    assert test_faiss_engine.total_vectors == len(sample_vectors)

    # Search with the first vector (should retrieve itself with similarity ~1.0)
    query_vec = sample_vectors[0]
    results = test_faiss_engine.search(query_vec, top_k=3)
    assert len(results) == 3
    top_score, top_meta, top_idx = results[0]
    assert np.isclose(top_score, 1.0, atol=1e-4)
    assert top_meta["id"] == 0


def test_faiss_engine_persistence(temp_dir, sample_vectors):
    import os
    from src.indexing.faiss_engine import FaissIndexEngine

    idx_file = os.path.join(temp_dir, "persist.index")
    meta_file = os.path.join(temp_dir, "persist.pkl")

    engine1 = FaissIndexEngine(dimension=384, index_file=idx_file, meta_file=meta_file)
    meta = [{"label": "Chunk A"}]
    engine1.add_vectors(sample_vectors[:1], meta)
    assert engine1.total_vectors == 1

    # Reload from disk into engine2
    engine2 = FaissIndexEngine(dimension=384, index_file=idx_file, meta_file=meta_file)
    assert engine2.total_vectors == 1
    assert engine2.metadata[0]["label"] == "Chunk A"


def test_faiss_engine_reset(test_faiss_engine, sample_vectors):
    meta = [{"label": "Chunk 1"}]
    test_faiss_engine.add_vectors(sample_vectors[:1], meta)
    assert test_faiss_engine.total_vectors == 1

    test_faiss_engine.reset()
    assert test_faiss_engine.total_vectors == 0
    assert len(test_faiss_engine.metadata) == 0
