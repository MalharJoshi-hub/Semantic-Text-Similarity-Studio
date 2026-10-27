"""In-memory vector and search query caching with LRU eviction."""

import hashlib
import time
from typing import Dict, Any, Optional, Tuple
import numpy as np


class VectorCache:
    """Least-Recently-Used (LRU) cache for embedding vectors and similarity results."""

    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self._cache: Dict[str, Tuple[float, Any]] = {}

    @staticmethod
    def hash_text(text: str) -> str:
        """Compute deterministic SHA-256 hash for text."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def get(self, text: str) -> Optional[np.ndarray]:
        """Retrieve cached vector if available, updating access timestamp."""
        key = self.hash_text(text)
        if key in self._cache:
            _, vec = self._cache[key]
            self._cache[key] = (time.time(), vec)
            return vec.copy()
        return None

    def put(self, text: str, vector: np.ndarray):
        """Insert vector into cache with LRU eviction when capacity is reached."""
        key = self.hash_text(text)
        if len(self._cache) >= self.max_size and key not in self._cache:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][0])
            del self._cache[oldest_key]
        self._cache[key] = (time.time(), vector.copy())

    def clear(self):
        """Purge all cached items."""
        self._cache.clear()

    @property
    def size(self) -> int:
        return len(self._cache)
