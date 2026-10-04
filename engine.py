"""
Semantic Similarity Engine.
Features:
- SentenceTransformer all-MiniLM-L6-v2 loaded once as singleton
- L2-normalized embeddings for strict Cosine Similarity via Inner Product
- FAISS IndexFlatIP per-chunk indexing with metadata persistence
- Pair similarity scoring with qualitative classification
- Corpus query search with top-k ranking and score clamping [0.0, 1.0]
"""

import pickle
import threading
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from chunker import chunk_text
import database

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
FAISS_INDEX_PATH = DATA_DIR / "similarity_faiss.index"
META_PATH = DATA_DIR / "similarity_meta.pkl"

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
EMB_DIM = 384

_model_lock = threading.Lock()
_model_instance = None

def get_model() -> SentenceTransformer:
    """Loads and caches SentenceTransformer model once."""
    global _model_instance
    if _model_instance is None:
        with _model_lock:
            if _model_instance is None:
                _model_instance = SentenceTransformer(EMBED_MODEL_NAME)
    return _model_instance

def embed_texts(texts: List[str]) -> np.ndarray:
    """
    Computes L2-normalized embeddings for a list of texts.
    Returns float32 2D numpy array of shape (N, EMB_DIM).
    """
    if not texts:
        return np.empty((0, EMB_DIM), dtype="float32")
    
    model = get_model()
    # Normalize embeddings directly
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms[norms == 0] = 1e-9
    normalized = embeddings / norms
    return normalized.astype("float32")

def get_similarity_label(score: float) -> Tuple[str, str, str]:
    """
    Returns (label, color_code, description) based on cosine similarity score [0.0, 1.0].
    """
    if score >= 0.85:
        return (
            "Extremely High Similarity",
            "#10b981",  # emerald
            "The texts express nearly identical or directly synonymous meaning."
        )
    elif score >= 0.70:
        return (
            "High Semantic Similarity",
            "#34d399",  # light emerald
            "Strong contextual and conceptual overlap with matching themes."
        )
    elif score >= 0.50:
        return (
            "Moderate Semantic Overlap",
            "#f59e0b",  # amber
            "Shared topic or partial conceptual relationship, but notable divergence in focus."
        )
    elif score >= 0.30:
        return (
            "Low / Weak Relevance",
            "#fb923c",  # orange
            "Minor topical connection or isolated overlapping terms, largely distinct intent."
        )
    else:
        return (
            "Unrelated / Distinct",
            "#94a3b8",  # slate
            "No significant semantic or contextual relationship detected."
        )

class SimilarityIndex:
    """
    Manages FAISS IndexFlatIP and chunk metadata.
    """
    def __init__(self):
        self.lock = threading.Lock()
        self.index = faiss.IndexFlatIP(EMB_DIM)
        # metadata maps index integer position -> chunk dict
        self.metadata: List[Dict[str, Any]] = []
        self._load()

    def _save(self):
        faiss.write_index(self.index, str(FAISS_INDEX_PATH))
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadata, f)

    def _load(self):
        if FAISS_INDEX_PATH.exists() and META_PATH.exists():
            try:
                self.index = faiss.read_index(str(FAISS_INDEX_PATH))
                with open(META_PATH, "rb") as f:
                    self.metadata = pickle.load(f)
            except Exception as e:
                print(f"[SimilarityIndex] Warning loading index: {e}, resetting index.")
                self.index = faiss.IndexFlatIP(EMB_DIM)
                self.metadata = []

    def add_document(self, text_id: int, doc_label: str, chunks: List[str]):
        """
        Embeds chunks and adds them to FAISS index and metadata.
        """
        if not chunks:
            return

        with self.lock:
            embs = embed_texts(chunks)
            self.index.add(embs)
            for idx, c_text in enumerate(chunks):
                self.metadata.append({
                    "text_id": text_id,
                    "doc_label": doc_label,
                    "chunk_index": idx,
                    "chunk_text": c_text
                })
            self._save()

    def rebuild_from_db(self):
        """
        Rebuilds FAISS index completely from SQLite database chunks.
        """
        with self.lock:
            all_chunks = database.get_all_chunks()
            new_index = faiss.IndexFlatIP(EMB_DIM)
            new_meta = []

            if all_chunks:
                texts = [c["chunk_text"] for c in all_chunks]
                embs = embed_texts(texts)
                new_index.add(embs)
                for c in all_chunks:
                    new_meta.append({
                        "chunk_id": c["chunk_id"],
                        "text_id": c["text_id"],
                        "doc_label": c["doc_label"],
                        "chunk_index": c["chunk_index"],
                        "chunk_text": c["chunk_text"]
                    })

            self.index = new_index
            self.metadata = new_meta
            self._save()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Searches the FAISS index for top_k most similar chunks.
        """
        query = query.strip()
        if not query or self.index.ntotal == 0:
            return []

        top_k = min(top_k, self.index.ntotal)
        q_emb = embed_texts([query])

        with self.lock:
            distances, indices = self.index.search(q_emb, top_k)

        results = []
        for rank, (score_raw, idx) in enumerate(zip(distances[0], indices[0]), start=1):
            if idx < 0 or idx >= len(self.metadata):
                continue
            meta = self.metadata[idx]
            # Clamp cosine score to [0.0, 1.0]
            clamped_score = float(np.clip(score_raw, 0.0, 1.0))
            score_rounded = round(clamped_score, 4)
            pct = round(clamped_score * 100, 1)
            label, color, desc = get_similarity_label(clamped_score)

            results.append({
                "rank": rank,
                "text_id": meta["text_id"],
                "doc_label": meta["doc_label"],
                "chunk_index": meta["chunk_index"],
                "score": score_rounded,
                "score_pct": pct,
                "label": label,
                "color": color,
                "description": desc,
                "snippet": meta["chunk_text"]
            })

        return results

    def get_stats(self) -> Dict[str, Any]:
        """Returns engine statistics."""
        return {
            "model_name": EMBED_MODEL_NAME,
            "embedding_dimension": EMB_DIM,
            "total_indexed_chunks": self.index.ntotal,
            "total_metadata_records": len(self.metadata)
        }

# Global singleton similarity index
similarity_index = SimilarityIndex()

def compute_pair_similarity(text1: str, text2: str) -> Dict[str, Any]:
    """
    Computes pairwise semantic similarity between two texts.
    Returns cosine similarity score clamped to [0.0, 1.0], percentage, qualitative label, and stats.
    """
    t1 = text1.strip()
    t2 = text2.strip()
    if not t1 or not t2:
        return {
            "score": 0.0,
            "score_pct": 0.0,
            "label": "Empty Input",
            "color": "#94a3b8",
            "description": "Please provide both texts to compute semantic similarity.",
            "text1_words": len(t1.split()),
            "text2_words": len(t2.split()),
            "text1_chars": len(t1),
            "text2_chars": len(t2)
        }

    embs = embed_texts([t1, t2])
    # Dot product of normalized vectors = Cosine similarity
    raw_score = float(np.dot(embs[0], embs[1]))
    score = float(np.clip(raw_score, 0.0, 1.0))
    score_rounded = round(score, 4)
    pct = round(score * 100, 1)
    label, color, desc = get_similarity_label(score)

    words1 = set(t1.lower().split())
    words2 = set(t2.lower().split())
    common_words = sorted(list(words1.intersection(words2)))

    return {
        "score": score_rounded,
        "score_pct": pct,
        "label": label,
        "color": color,
        "description": desc,
        "text1_words": len(t1.split()),
        "text2_words": len(t2.split()),
        "text1_chars": len(t1),
        "text2_chars": len(t2),
        "common_words_count": len(common_words),
        "common_words_sample": common_words[:12]
    }
