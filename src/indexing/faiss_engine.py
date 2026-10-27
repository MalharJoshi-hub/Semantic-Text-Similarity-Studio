"""FAISS Index Engine with thread-safe operations, persistence, and search."""

import os
import pickle
import threading
import logging
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import faiss

from src.core.normalization import normalize_l2, clamp_score

logger = logging.getLogger(__name__)

_GLOBAL_FAISS_LOCK = threading.Lock()
_GLOBAL_FAISS_INSTANCE = None


class FaissIndexEngine:
    """Encapsulates a faiss.IndexFlatIP index with synchronization and metadata mappings."""

    def __init__(self, dimension: int = 384, index_file: str = "data/similarity_faiss.index", meta_file: str = "data/similarity_meta.pkl"):
        self.dimension = dimension
        self.index_file = index_file
        self.meta_file = meta_file
        self._lock = threading.Lock()
        self.index: Optional[faiss.IndexFlatIP] = None
        self.metadata: List[Dict[str, Any]] = []
        self._load_or_create()

    def _load_or_create(self):
        """Load persisted index from disk or initialize a new empty IndexFlatIP."""
        with self._lock:
            os.makedirs(os.path.dirname(os.path.abspath(self.index_file)), exist_ok=True)
            if os.path.exists(self.index_file) and os.path.exists(self.meta_file):
                try:
                    logger.info("Loading existing FAISS index from %s", self.index_file)
                    self.index = faiss.read_index(self.index_file)
                    with open(self.meta_file, "rb") as f:
                        self.metadata = pickle.load(f)
                    logger.info("Loaded FAISS index with %d vectors", self.index.ntotal)
                    return
                except Exception as e:
                    logger.warning("Failed to load FAISS index from disk (%s). Recreating...", e)

            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata = []
            logger.info("Initialized new empty faiss.IndexFlatIP(dim=%d)", self.dimension)

    def save(self):
        """Atomically persist current index and metadata cache to disk."""
        with self._lock:
            temp_idx = f"{self.index_file}.tmp"
            temp_meta = f"{self.meta_file}.tmp"
            faiss.write_index(self.index, temp_idx)
            with open(temp_meta, "wb") as f:
                pickle.dump(self.metadata, f)
            if os.path.exists(self.index_file):
                os.remove(self.index_file)
            if os.path.exists(self.meta_file):
                os.remove(self.meta_file)
            os.rename(temp_idx, self.index_file)
            os.rename(temp_meta, self.meta_file)

    @property
    def total_vectors(self) -> int:
        with self._lock:
            return self.index.ntotal if self.index else 0

    def add_vectors(self, vectors: np.ndarray, meta_records: List[Dict[str, Any]]) -> List[int]:
        """Add normalized vectors and corresponding metadata records to FAISS.

        Args:
            vectors: np.ndarray of shape (N, d) or (d,).
            meta_records: List of dict metadata for each vector.

        Returns:
            List of starting vector IDs assigned in FAISS.
        """
        arr = np.asarray(vectors, dtype=np.float32)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        if arr.shape[1] != self.dimension:
            raise ValueError(f"Vector dim {arr.shape[1]} does not match index dim {self.dimension}")

        norm_arr = normalize_l2(arr)
        count = norm_arr.shape[0]
        if len(meta_records) != count:
            raise ValueError(f"Metadata count ({len(meta_records)}) != vector count ({count})")

        with self._lock:
            start_id = self.index.ntotal
            self.index.add(norm_arr)
            self.metadata.extend(meta_records)
            assigned_ids = list(range(start_id, start_id + count))

        self.save()
        return assigned_ids

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[float, Dict[str, Any], int]]:
        """Search top-k most similar vectors in the FAISS index.

        Args:
            query_vector: 1D vector (dim,) or 2D vector (1, dim).
            top_k: Number of nearest neighbors to retrieve.

        Returns:
            List of tuples: (clamped_cosine_score, metadata_dict, vector_id).
        """
        arr = np.asarray(query_vector, dtype=np.float32)
        if arr.ndim == 1:
            arr = arr.reshape(1, -1)
        norm_query = normalize_l2(arr)

        with self._lock:
            total = self.index.ntotal
            if total == 0:
                return []
            k = min(top_k, total)
            distances, indices = self.index.search(norm_query, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            score = clamp_score(float(dist))
            meta = self.metadata[idx]
            results.append((score, meta, int(idx)))

        return results

    def reset(self):
        """Reset index and metadata to empty state and clear disk caches."""
        with self._lock:
            self.index = faiss.IndexFlatIP(self.dimension)
            self.metadata = []
            for path in [self.index_file, self.meta_file]:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass
            logger.info("Reset FAISS index and cleared disk files")


def get_faiss_engine(dimension: int = 384) -> FaissIndexEngine:
    """Thread-safe factory returning global FAISS engine singleton."""
    global _GLOBAL_FAISS_INSTANCE
    if _GLOBAL_FAISS_INSTANCE is None:
        with _GLOBAL_FAISS_LOCK:
            if _GLOBAL_FAISS_INSTANCE is None:
                _GLOBAL_FAISS_INSTANCE = FaissIndexEngine(dimension=dimension)
    return _GLOBAL_FAISS_INSTANCE
