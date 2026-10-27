"""Unit tests for VectorStore coordinating embeddings and FAISS."""

import pytest
from src.indexing.vector_store import VectorStore


def test_vector_store_index_and_search(test_faiss_engine):
    vs = VectorStore(indexer=test_faiss_engine)
    chunks = [
        {"id": 1, "chunk_index": 0, "content": "The quick brown fox jumps over the lazy dog.", "section_title": "Intro"},
        {"id": 2, "chunk_index": 1, "content": "Modern cloud computing relies on containerization.", "section_title": "Cloud"},
    ]
    ids = vs.index_chunks(doc_id=10, doc_title="Sample Document", chunks=chunks)
    assert len(ids) == 2

    # Query search
    results = vs.search("canine jumping over animal", top_k=2)
    assert len(results) == 2
    # The first result should be the fox sentence
    assert results[0].doc_title == "Sample Document"
    assert "fox" in results[0].content
    assert results[0].score > 0.4


def test_vector_store_search_empty():
    vs = VectorStore()
    results = vs.search("")
    assert results == []
