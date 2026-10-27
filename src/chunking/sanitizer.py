"""Text sanitization and unicode normalization."""

import re
import unicodedata


def sanitize_document_text(text: str) -> str:
    """Clean raw document text by normalizing unicode, carriage returns, and control characters."""
    if not text:
        return ""

    # Normalize unicode to NFKC form
    cleaned = unicodedata.normalize("NFKC", text)

    # Standardize newlines
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")

    # Strip null bytes and non-printable control characters except tab and newline
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", cleaned)

    # Normalize trailing spaces on lines
    cleaned = re.sub(r"[ \t]+$", "", cleaned, flags=re.MULTILINE)

    # Collapse excessive consecutive newlines (> 3) to 2 newlines
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()
