"""Sentence Transformer model singleton, encoding, and vectorization engine."""

import logging
import threading
from typing import List, Union
import numpy as np

logger = logging.getLogger(__name__)

_GLOBAL_ENGINE_LOCK = threading.Lock()
_GLOBAL_ENGINE_INSTANCE = None


class EmbeddingEngine:
    """Thread-safe singleton wrapper around sentence-transformers/all-MiniLM-L6-v2."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._lock = threading.Lock()
        self._model = None
        self._dimension = 384
        logger.info("Initializing EmbeddingEngine with model: %s", model_name)

    def _ensure_loaded(self):
        """Lazy load the transformer model weights on demand."""
        if self._model is None:
            with self._lock:
                if self._model is None:
                    from sentence_transformers import SentenceTransformer
                    logger.info("Loading SentenceTransformer model weights for %s...", self.model_name)
                    self._model = SentenceTransformer(self.model_name)
                    self._dimension = self._model.get_sentence_embedding_dimension()
                    logger.info("SentenceTransformer loaded successfully. Dimension: %d", self._dimension)

    @property
    def dimension(self) -> int:
        return self._dimension

    def encode(self, texts: Union[str, List[str]], batch_size: int = 32, normalize: bool = True) -> np.ndarray:
        """Encode single text or list of texts into L2-normalized numpy vectors.

        Args:
            texts: Single string or sequence of text strings.
            batch_size: Mini-batch size for transformer inference.
            normalize: If True, normalize outputs to unit L2 norm.

        Returns:
            np.ndarray of shape (d,) for single string or (N, d) for list.
        """
        self._ensure_loaded()
        single = isinstance(texts, str)
        inputs = [texts] if single else list(texts)

        if not inputs:
            return np.empty((0, self._dimension), dtype=np.float32)

        with self._lock:
            embeddings = self._model.encode(
                inputs,
                batch_size=batch_size,
                show_progress_bar=False,
                convert_to_numpy=True,
                normalize_embeddings=normalize,
            )

        embeddings = np.asarray(embeddings, dtype=np.float32)
        if single:
            return embeddings[0]
        return embeddings


def get_embedding_engine(model_name: str = "all-MiniLM-L6-v2") -> EmbeddingEngine:
    """Global factory function returning the thread-safe singleton EmbeddingEngine."""
    global _GLOBAL_ENGINE_INSTANCE
    if _GLOBAL_ENGINE_INSTANCE is None:
        with _GLOBAL_ENGINE_LOCK:
            if _GLOBAL_ENGINE_INSTANCE is None:
                _GLOBAL_ENGINE_INSTANCE = EmbeddingEngine(model_name)
    return _GLOBAL_ENGINE_INSTANCE
