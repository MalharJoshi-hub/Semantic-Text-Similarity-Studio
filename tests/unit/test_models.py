"""Unit tests for storage models and serialization contracts."""

import pytest
from src.storage.models import TextRecord, ChunkRecord, CorpusStats


def test_chunk_record_to_dict():
    chunk = ChunkRecord(
        id=1,
        text_id=10,
        chunk_index=0,
        chunk_text="Test chunk text content.",
        char_count=25,
        word_count=4,
        section_title="Intro",
    )
    d = chunk.to_dict()
    assert d["id"] == 1
    assert d["text_id"] == 10
    assert d["chunk_text"] == "Test chunk text content."
    assert d["section_title"] == "Intro"


def test_text_record_to_dict():
    text = TextRecord(
        id=5,
        label="Document Title",
        content="Full document text",
        source_type="markdown",
        char_count=18,
        word_count=3,
        chunk_count=1,
        created_at="2026-10-27 10:00:00 UTC",
    )
    d = text.to_dict(include_chunks=False)
    assert d["id"] == 5
    assert d["label"] == "Document Title"
    assert "content" not in d

    d_full = text.to_dict(include_chunks=True)
    assert d_full["content"] == "Full document text"
    assert "chunks" in d_full


def test_corpus_stats():
    stats = CorpusStats(total_texts=5, total_chunks=25, total_words=5000)
    d = stats.to_dict()
    assert d["total_texts"] == 5
    assert d["total_chunks"] == 25
    assert d["total_words"] == 5000
