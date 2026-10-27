"""Vector store abstraction coordinating embedding generation, FAISS indexing, and persistence."""

import logging
from typing import List, Dict, Any, Optional
import numpy as np

from src.core.embeddings import EmbeddingEngine, get_embedding_engine
from src.indexing.faiss_engine import FaissIndexEngine, get_faiss_engine
from src.core.types import SearchResult, TierInfo
from src.core.similarity import classify_similarity_tier

logger = logging.getLogger(__name__)


class VectorStore:
    """Orchestrates embedding models, vector indices, and document-chunk metadata."""

    def __init__(self, embedder: Optional[EmbeddingEngine] = None, indexer: Optional[FaissIndexEngine] = None):
        self.embedder = embedder or get_embedding_engine()
        self.indexer = indexer or get_faiss_engine(dimension=self.embedder.dimension)

    def index_chunks(self, doc_id: int, doc_title: str, chunks: List[Dict[str, Any]]) -> List[int]:
        """Generate vectors for chunks and register them into the FAISS index."""
        if not chunks:
            return []

        texts = [c["content"] for c in chunks]
        vectors = self.embedder.encode(texts, normalize=True)

        meta_records = []
        for idx, chunk in enumerate(chunks):
            meta_records.append({
                "doc_id": doc_id,
                "doc_title": doc_title,
                "chunk_id": chunk.get("id"),
                "chunk_index": chunk.get("chunk_index", idx),
                "section_title": chunk.get("section_title", "General"),
                "content": chunk["content"],
                "word_count": chunk.get("word_count", len(chunk["content"].split())),
            })

        assigned_ids = self.indexer.add_vectors(vectors, meta_records)
        return assigned_ids

    def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """Perform semantic search for query string across the indexed corpus."""
        if not query.strip() or self.indexer.total_vectors == 0:
            return []

        query_vec = self.embedder.encode(query, normalize=True)
        raw_matches = self.indexer.search(query_vec, top_k=top_k)

        results = []
        for score, meta, vector_id in raw_matches:
            tier_name, tier_color, _ = classify_similarity_tier(score)
            results.append(SearchResult(
                chunk_id=meta.get("chunk_id", vector_id),
                doc_id=meta.get("doc_id", 0),
                doc_title=meta.get("doc_title", "Unknown"),
                section_title=meta.get("section_title", "General"),
                chunk_index=meta.get("chunk_index", 0),
                content=meta.get("content", ""),
                score=score,
                percentage=score * 100.0,
                tier=tier_name,
                color=tier_color,
            ))

        return results

    def rebuild_index(self, all_chunks_with_doc_info: List[Dict[str, Any]]):
        """Idempotently rebuild entire FAISS index from stored database chunks."""
        logger.info("Rebuilding vector store index with %d chunks...", len(all_chunks_with_doc_info))
        self.indexer.reset()
        if not all_chunks_with_doc_info:
            return

        texts = [c["content"] for c in all_chunks_with_doc_info]
        vectors = self.embedder.encode(texts, batch_size=64, normalize=True)

        meta_records = []
        for c in all_chunks_with_doc_info:
            meta_records.append({
                "doc_id": c.get("doc_id"),
                "doc_title": c.get("doc_title", "Unknown"),
                "chunk_id": c.get("id"),
                "chunk_index": c.get("chunk_index", 0),
                "section_title": c.get("section_title", "General"),
                "content": c.get("content", ""),
                "word_count": c.get("word_count", 0),
            })

        self.indexer.add_vectors(vectors, meta_records)
        logger.info("Index rebuild complete. Total vectors: %d", self.indexer.total_vectors)
