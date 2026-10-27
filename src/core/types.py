"""Type definitions, dataclasses, and data contracts for core NLP operations."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import numpy as np


@dataclass(frozen=True)
class TierInfo:
    """Qualitative classification tier definition."""
    tier: str
    color: str
    description: str
    threshold_min: float
    threshold_max: float


@dataclass
class SimilarityResult:
    """Pairwise similarity computation output contract."""
    cosine_similarity: float
    percentage: float
    lexical_overlap: float
    tier: str
    color: str
    tier_description: str
    text1_word_count: int
    text2_word_count: int
    text1_char_count: int
    text2_char_count: int
    computation_time_ms: float
    vector_dimension: int = 384
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert dataclass to standard JSON serializable dictionary."""
        return {
            "cosine_similarity": round(self.cosine_similarity, 4),
            "percentage": round(self.percentage, 1),
            "lexical_overlap": round(self.lexical_overlap, 4),
            "tier": self.tier,
            "color": self.color,
            "tier_description": self.tier_description,
            "text1_word_count": self.text1_word_count,
            "text2_word_count": self.text2_word_count,
            "text1_char_count": self.text1_char_count,
            "text2_char_count": self.text2_char_count,
            "computation_time_ms": round(self.computation_time_ms, 2),
            "vector_dimension": self.vector_dimension,
            "metadata": self.metadata,
        }


@dataclass
class ChunkRecord:
    """Document chunk record representation."""
    chunk_index: int
    section_title: str
    content: str
    word_count: int
    char_count: int
    vector_id: Optional[int] = None
    doc_id: Optional[int] = None
    similarity_score: Optional[float] = None


@dataclass
class SearchResult:
    """FAISS retrieval match record."""
    chunk_id: int
    doc_id: int
    doc_title: str
    section_title: str
    chunk_index: int
    content: str
    score: float
    percentage: float
    tier: str
    color: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "doc_id": self.doc_id,
            "doc_title": self.doc_title,
            "section_title": self.section_title,
            "chunk_index": self.chunk_index,
            "content": self.content,
            "score": round(self.score, 4),
            "percentage": round(self.percentage, 1),
            "tier": self.tier,
            "color": self.color,
        }
