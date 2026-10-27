"""Vector quantization utilities for scalable memory reduction."""

import numpy as np
from typing import Tuple


class ScalarQuantizer:
    """8-bit uniform scalar quantizer reducing float32 vector memory footprint by 4x."""

    def __init__(self, n_bits: int = 8):
        self.n_bits = n_bits
        self.q_levels = 2 ** n_bits - 1

    def quantize(self, vectors: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Quantize float32 vectors into uint8 arrays along with scale and min offset.

        Returns:
            quantized: uint8 array
            mins: float32 minimum per vector
            ranges: float32 dynamic range per vector
        """
        arr = np.asarray(vectors, dtype=np.float32)
        mins = arr.min(axis=-1, keepdims=True)
        maxs = arr.max(axis=-1, keepdims=True)
        ranges = np.maximum(maxs - mins, 1e-9)

        normalized = (arr - mins) / ranges
        quantized = np.clip(np.round(normalized * self.q_levels), 0, self.q_levels).astype(np.uint8)
        return quantized, mins.squeeze(-1), ranges.squeeze(-1)

    def dequantize(self, quantized: np.ndarray, mins: np.ndarray, ranges: np.ndarray) -> np.ndarray:
        """Reconstruct approximate float32 vectors from quantized representation."""
        q = np.asarray(quantized, dtype=np.float32)
        mins = np.asarray(mins, dtype=np.float32)
        ranges = np.asarray(ranges, dtype=np.float32)

        if q.ndim == 1:
            return mins + (q / self.q_levels) * ranges
        return mins[:, np.newaxis] + (q / self.q_levels) * ranges[:, np.newaxis]
