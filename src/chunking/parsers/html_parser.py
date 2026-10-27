"""HTML text extractor stripping tags while preserving structure."""

import re
from typing import Dict, Any


def parse_html(html_text: str) -> Dict[str, Any]:
    """Parse HTML string and extract clean text preserving header breaks."""
    title_match = re.search(r"<title>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else "Untitled HTML Page"

    # Remove script and style tags
    clean = re.sub(r"<(script|style).*?>.*?</\1>", "", html_text, flags=re.IGNORECASE | re.DOTALL)

    # Convert headers and paragraph breaks to newlines
    clean = re.sub(r"<(h[1-6]|p|div|br|li)[^>]*>", "\n", clean, flags=re.IGNORECASE)

    # Strip remaining HTML tags
    clean = re.sub(r"<[^>]+>", "", clean)

    # Clean whitespace
    lines = [l.strip() for l in clean.split("\n") if l.strip()]
    return {
        "title": title,
        "content": "\n\n".join(lines),
        "format": "html",
    }
