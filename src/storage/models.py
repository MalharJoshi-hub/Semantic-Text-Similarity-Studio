"""Data models and entities for persistence layer."""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class ChunkRecord:
    """Represents a persisted text chunk in SQLite."""
    id: Optional[int]
    text_id: int
    chunk_index: int
    chunk_text: str
    char_count: int
    word_count: int
    section_title: Optional[str] = "General"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text_id": self.text_id,
            "chunk_index": self.chunk_index,
            "chunk_text": self.chunk_text,
            "char_count": self.char_count,
            "word_count": self.word_count,
            "section_title": self.section_title,
        }


@dataclass
class TextRecord:
    """Represents a persisted parent document in SQLite."""
    id: Optional[int]
    label: str
    content: str
    source_type: str = "text"
    char_count: int = 0
    word_count: int = 0
    chunk_count: int = 0
    created_at: str = ""
    chunks: List[ChunkRecord] = field(default_factory=list)

    def to_dict(self, include_chunks: bool = False) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "label": self.label,
            "source_type": self.source_type,
            "char_count": self.char_count,
            "word_count": self.word_count,
            "chunk_count": self.chunk_count,
            "created_at": self.created_at,
        }
        if include_chunks:
            data["content"] = self.content
            data["chunks"] = [c.to_dict() for c in self.chunks]
        return data


@dataclass
class CorpusStats:
    """Summary corpus telemetry metrics."""
    total_texts: int
    total_chunks: int
    total_words: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_texts": self.total_texts,
            "total_chunks": self.total_chunks,
            "total_words": self.total_words,
        }
