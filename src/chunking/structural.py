"""Structural section and header-aware document chunker."""

import re
from typing import List, Dict, Any, Optional

HEADER_PATTERN = re.compile(
    r'(?m)^(?:\s*#{1,6}\s+(.+?)\s*$|\s*(?:Section|Chapter|\d+\.|\d+\.\d+|\d+\))\s+(.+?)\s*$|\s*([A-Z0-9\s\-_:,.]{3,60})\s*$)'
)


class StructuralChunker:
    """Header-aware document chunker preserving structural boundaries."""

    def __init__(self, max_words: int = 150, overlap_words: int = 30, min_section_words: int = 20):
        self.max_words = max_words
        self.overlap_words = overlap_words
        self.min_section_words = min_section_words

    def extract_header_title(self, line: str) -> Optional[str]:
        """Check if line is a structural header and extract its clean title."""
        stripped = line.strip()
        if not stripped or len(stripped.split()) > 14:
            return None
        match = HEADER_PATTERN.match(line)
        if match:
            for group in match.groups():
                if group:
                    return group.strip("# \t\r\n")
            return stripped
        return None

    def partition_sections(self, text: str) -> List[Dict[str, Any]]:
        """Split document into sections labeled with detected header titles."""
        clean_text = text.replace("\r\n", "\n").strip()
        if not clean_text:
            return []

        lines = clean_text.split("\n")
        sections = []
        current_title = "Introduction"
        current_lines = []

        for line in lines:
            header = self.extract_header_title(line)
            if header:
                if current_lines:
                    content = "\n".join(current_lines).strip()
                    if content:
                        sections.append({"title": current_title, "content": content})
                    current_lines = []
                current_title = header
            else:
                current_lines.append(line)

        if current_lines:
            content = "\n".join(current_lines).strip()
            if content:
                sections.append({"title": current_title, "content": content})

        if not sections and clean_text:
            sections.append({"title": "General", "content": clean_text})

        return sections

    def chunk_document(self, text: str) -> List[Dict[str, Any]]:
        """Full structural chunking returning list of chunk dicts with metadata."""
        sections = self.partition_sections(text)
        chunks = []
        chunk_idx = 0

        for sec in sections:
            sec_title = sec["title"]
            content = sec["content"]
            words = content.split()

            if len(words) <= self.max_words:
                chunks.append({
                    "chunk_index": chunk_idx,
                    "section_title": sec_title,
                    "content": content,
                    "word_count": len(words),
                    "char_count": len(content),
                })
                chunk_idx += 1
            else:
                # Sliding window within section
                start = 0
                step = max(1, self.max_words - self.overlap_words)
                sub_idx = 1
                while start < len(words):
                    sub_words = words[start:start + self.max_words]
                    sub_text = " ".join(sub_words).strip()
                    sub_title = f"{sec_title} (Part {sub_idx})" if sub_idx > 1 else sec_title

                    chunks.append({
                        "chunk_index": chunk_idx,
                        "section_title": sub_title,
                        "content": sub_text,
                        "word_count": len(sub_words),
                        "char_count": len(sub_text),
                    })
                    chunk_idx += 1
                    sub_idx += 1

                    if start + self.max_words >= len(words):
                        break
                    start += step

        return chunks


def create_structural_chunker(max_words: int = 150, overlap_words: int = 30) -> StructuralChunker:
    return StructuralChunker(max_words=max_words, overlap_words=overlap_words)
