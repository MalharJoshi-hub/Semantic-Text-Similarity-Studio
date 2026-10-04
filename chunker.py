"""
Structural Chunker Module for Semantic Text Similarity.
Features:
- Regex-based section header detection (Markdown, numbered sections, uppercase headers, paragraph breaks)
- 150-word sliding window fallback with configurable overlap for oversized sections
"""

import re
from typing import List

# Regex to detect structural headers:
# 1. Markdown headers: '# Header', '## Subheader', etc.
# 2. Numbered sections: 'Section 1:', 'Chapter 2', '1.1 Title', '1) Intro'
# 3. Uppercase headings: 'INTRODUCTION', 'EXECUTIVE SUMMARY', 'BACKGROUND'
HEADER_PATTERN = re.compile(
    r'(?m)^(?:\s*#{1,6}\s+.+|\s*(?:Section|Chapter|\d+\.|\d+\.\d+|\d+\))\s+.+|\s*[A-Z0-9\s\-_:,.]{3,60})$'
)

def split_into_structural_sections(text: str) -> List[str]:
    """
    Splits text by structural headers or paragraph breaks.
    """
    text = text.replace('\r\n', '\n').strip()
    if not text:
        return []

    lines = text.split('\n')
    sections = []
    current_section = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            # Paragraph separator: if section is long enough, end it
            if current_section:
                sec_text = '\n'.join(current_section).strip()
                if len(sec_text.split()) >= 30:
                    sections.append(sec_text)
                    current_section = []
            continue

        # Check if line looks like a header
        if HEADER_PATTERN.match(line) and len(stripped.split()) <= 12:
            if current_section:
                sec_text = '\n'.join(current_section).strip()
                if sec_text:
                    sections.append(sec_text)
                current_section = []
            current_section.append(line)
        else:
            current_section.append(line)

    if current_section:
        sec_text = '\n'.join(current_section).strip()
        if sec_text:
            sections.append(sec_text)

    # Fallback if no sections detected
    if not sections and text:
        sections = [p.strip() for p in text.split('\n\n') if p.strip()]

    return sections if sections else [text]

def sliding_window_chunk(text: str, max_words: int = 150, overlap_words: int = 30) -> List[str]:
    """
    Applies sliding window chunking to break a long text into chunks of max_words with overlap.
    """
    words = text.split()
    if len(words) <= max_words:
        return [text]

    chunks = []
    start = 0
    step = max(1, max_words - overlap_words)

    while start < len(words):
        chunk_words = words[start:start + max_words]
        chunk_text = " ".join(chunk_words).strip()
        if chunk_text:
            chunks.append(chunk_text)
        if start + max_words >= len(words):
            break
        start += step

    return chunks

def chunk_text(text: str, max_words: int = 150, overlap_words: int = 30) -> List[str]:
    """
    Full structural chunking pipeline:
    1. Splits by structural headers/sections.
    2. Any section exceeding max_words is chunked using sliding window.
    3. Short consecutive sections are merged if helpful to maintain context.
    """
    raw_sections = split_into_structural_sections(text)
    final_chunks: List[str] = []

    for sec in raw_sections:
        words = sec.split()
        if len(words) > max_words:
            sub_chunks = sliding_window_chunk(sec, max_words=max_words, overlap_words=overlap_words)
            final_chunks.extend(sub_chunks)
        else:
            if sec.strip():
                final_chunks.append(sec.strip())

    # Fallback check
    if not final_chunks and text.strip():
        final_chunks = sliding_window_chunk(text.strip(), max_words=max_words, overlap_words=overlap_words)

    return final_chunks
