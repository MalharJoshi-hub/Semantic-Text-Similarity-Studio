"""Unit tests for text sanitization and normalization."""

import pytest
from src.chunking.sanitizer import sanitize_document_text


def test_sanitize_empty():
    assert sanitize_document_text("") == ""
    assert sanitize_document_text(None) == ""


def test_sanitize_crlf():
    text = "line 1\r\nline 2\rline 3\n"
    cleaned = sanitize_document_text(text)
    assert "\r" not in cleaned
    assert "line 1\nline 2\nline 3" == cleaned


def test_sanitize_control_chars():
    text = "clean\x00text\x07with\x08control\x1bchars"
    cleaned = sanitize_document_text(text)
    assert cleaned == "cleantextwithcontrolchars"


def test_sanitize_excessive_newlines():
    text = "paragraph 1\n\n\n\n\n\nparagraph 2"
    cleaned = sanitize_document_text(text)
    assert cleaned == "paragraph 1\n\nparagraph 2"
