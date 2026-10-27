"""Unit tests for ScalarQuantizer."""

import pytest
import numpy as np
from src.indexing.quantization import ScalarQuantizer


def test_scalar_quantizer_compression():
    sq = ScalarQuantizer(n_bits=8)
    vectors = np.random.randn(20, 384).astype(np.float32)

    quantized, mins, ranges = sq.quantize(vectors)
    assert quantized.dtype == np.uint8
    assert quantized.shape == (20, 384)

    # Reconstruct
    reconstructed = sq.dequantize(quantized, mins, ranges)
    assert reconstructed.dtype == np.float32
    assert reconstructed.shape == (20, 384)

    # Quantization error should be small (< 0.05 for uniform 8-bit)
    max_error = np.max(np.abs(vectors - reconstructed))
    mean_error = np.mean(np.abs(vectors - reconstructed))
    assert mean_error < 0.02
    assert max_error < 0.06
