"""Unit tests for token sliding window chunker."""

import pytest
from src.chunking.token_window import TokenWindowChunker


def test_token_window_basic():
    text = "one two three four five six seven eight nine ten"
    chunker = TokenWindowChunker(window_size=4, step_size=3)
    chunks = chunker.chunk(text)
    # Expected windows:
    # 1: one two three four (start 0, end 4)
    # 2: four five six seven (start 3, end 7)
    # 3: seven eight nine ten (start 6, end 10)
    assert len(chunks) == 3
    assert chunks[0] == "one two three four"
    assert chunks[1] == "four five six seven"
    assert chunks[2] == "seven eight nine ten"


def test_token_window_empty():
    chunker = TokenWindowChunker(window_size=10, step_size=5)
    assert chunker.chunk("") == []


def test_token_window_smaller_than_window():
    text = "short text here"
    chunker = TokenWindowChunker(window_size=10, step_size=5)
    chunks = chunker.chunk(text)
    assert len(chunks) == 1
    assert chunks[0] == text


def test_token_window_invalid_step():
    with pytest.raises(ValueError):
        TokenWindowChunker(window_size=10, step_size=0)
