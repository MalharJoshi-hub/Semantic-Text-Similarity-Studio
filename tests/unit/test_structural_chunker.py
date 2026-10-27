"""Unit tests for structural section and header-aware chunking."""

import pytest
from src.chunking.structural import StructuralChunker, create_structural_chunker


def test_header_detection_markdown():
    chunker = create_structural_chunker(max_words=150, overlap_words=30)
    assert chunker.extract_header_title("# Executive Summary") == "Executive Summary"
    assert chunker.extract_header_title("## Section 2.1 Overview") == "Section 2.1 Overview"
    assert chunker.extract_header_title("Not a header line with too many random words.") is None


def test_header_detection_numbered():
    chunker = create_structural_chunker()
    assert chunker.extract_header_title("Section 1: Introduction") is not None
    assert chunker.extract_header_title("1.1 Background") is not None


def test_partition_sections():
    text = """# Introduction
This is the introductory text for the document.

## Architecture
This section describes the five distinct layers of the system.
"""
    chunker = create_structural_chunker()
    sections = chunker.partition_sections(text)
    assert len(sections) == 2
    assert sections[0]["title"] == "Introduction"
    assert "introductory text" in sections[0]["content"]
    assert sections[1]["title"] == "Architecture"


def test_chunk_document_atomic_small():
    text = """# Short Document
This is a short section with fewer than 150 words.
"""
    chunker = create_structural_chunker(max_words=150)
    chunks = chunker.chunk_document(text)
    assert len(chunks) == 1
    assert chunks[0]["section_title"] == "Short Document"
    assert chunks[0]["chunk_index"] == 0


def test_chunk_document_sliding_window():
    # Generate 300 words
    words = [f"word{i}" for i in range(300)]
    text = f"# Long Document\n{' '.join(words)}"

    chunker = create_structural_chunker(max_words=100, overlap_words=20)
    chunks = chunker.chunk_document(text)
    assert len(chunks) > 1
    # Check that chunk indices are sequential
    for idx, c in enumerate(chunks):
        assert c["chunk_index"] == idx
        assert c["word_count"] <= 100
