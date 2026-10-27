"""Cryptographic SHA-256 content hashing utilities."""

import hashlib
from pathlib import Path
from typing import Union


def compute_text_hash(text: str) -> str:
    """Compute deterministic SHA-256 hash string for text content."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compute_file_hash(file_path: Union[str, Path]) -> str:
    """Compute SHA-256 hash for file on disk in streaming 64KB blocks."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()
