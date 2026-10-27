"""Markdown format structural parser."""

import re
from typing import Dict, Any, List


def parse_markdown(markdown_text: str) -> Dict[str, Any]:
    """Parse markdown text and extract title, sections, and metadata."""
    lines = markdown_text.strip().split("\n")
    title = "Untitled Markdown Document"

    # Find first level 1 or 2 header
    for line in lines:
        match = re.match(r"^#{1,2}\s+(.+)$", line.strip())
        if match:
            title = match.group(1).strip()
            break

    # Extract clean text without raw code fence tags
    clean_lines = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        clean_lines.append(line)

    return {
        "title": title,
        "content": "\n".join(clean_lines).strip(),
        "format": "markdown",
        "line_count": len(lines),
    }
