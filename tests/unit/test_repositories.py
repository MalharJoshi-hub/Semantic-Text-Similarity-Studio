"""Unit tests for TextRepository and ChunkRepository operations."""

import pytest


def test_text_repo_add_and_get(test_text_repo):
    chunks = ["First chunk.", "Second chunk.", "Third chunk."]
    rec = test_text_repo.add_text("Sample Doc", "Full content here", chunks, source_type="text")
    assert rec.id is not None
    assert rec.label == "Sample Doc"
    assert rec.chunk_count == 3

    fetched = test_text_repo.get_by_id(rec.id)
    assert fetched is not None
    assert fetched.label == "Sample Doc"
    assert len(fetched.chunks) == 3
    assert fetched.chunks[0].chunk_text == "First chunk."


def test_text_repo_list_and_stats(test_text_repo):
    test_text_repo.add_text("Doc 1", "Content 1", ["c1", "c2"])
    test_text_repo.add_text("Doc 2", "Content 2", ["c3"])

    all_docs = test_text_repo.list_all()
    assert len(all_docs) == 2

    stats = test_text_repo.get_stats()
    assert stats.total_texts == 2
    assert stats.total_chunks == 3


def test_text_repo_delete_cascade(test_text_repo, test_chunk_repo):
    rec = test_text_repo.add_text("Doc to Delete", "Content", ["chunk a", "chunk b"])
    doc_id = rec.id

    assert test_text_repo.delete(doc_id) is True
    assert test_text_repo.get_by_id(doc_id) is None

    # Check chunks table cascade delete
    all_chunks = test_chunk_repo.get_all_for_rebuild()
    assert len(all_chunks) == 0


def test_chunk_repo_rebuild(test_text_repo, test_chunk_repo):
    test_text_repo.add_text("Doc A", "Content A", ["chunk 1", "chunk 2"])
    test_text_repo.add_text("Doc B", "Content B", ["chunk 3"])

    rebuild_data = test_chunk_repo.get_all_for_rebuild()
    assert len(rebuild_data) == 3
    labels = [r["doc_label"] for r in rebuild_data]
    assert "Doc A" in labels
    assert "Doc B" in labels
