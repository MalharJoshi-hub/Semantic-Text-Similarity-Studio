"""Plaintext parser with heuristic title extraction."""

from typing import Dict, Any


def parse_plaintext(raw_text: str) -> Dict[str, Any]:
    """Parse plain text document and extract inferred title and statistics."""
    lines = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]
    title = lines[0][:80] if lines else "Untitled Text Document"

    words = raw_text.split()
    return {
        "title": title,
        "content": raw_text.strip(),
        "format": "text",
        "word_count": len(words),
        "char_count": len(raw_text),
    }
