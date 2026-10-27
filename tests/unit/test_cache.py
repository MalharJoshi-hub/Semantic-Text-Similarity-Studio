"""Unit tests for VectorCache LRU eviction."""

import pytest
import numpy as np
from src.indexing.cache import VectorCache


def test_vector_cache_put_get():
    cache = VectorCache(max_size=3)
    vec1 = np.array([1.0, 2.0], dtype=np.float32)
    cache.put("text 1", vec1)

    cached = cache.get("text 1")
    assert cached is not None
    assert np.allclose(cached, vec1)
    assert cache.get("non-existent") is None


def test_vector_cache_eviction():
    cache = VectorCache(max_size=2)
    cache.put("t1", np.array([1.0]))
    cache.put("t2", np.array([2.0]))
    # Access t1 to make t2 the least recently used
    cache.get("t1")
    # Put t3, should evict t2
    cache.put("t3", np.array([3.0]))

    assert cache.size == 2
    assert cache.get("t1") is not None
    assert cache.get("t3") is not None
    assert cache.get("t2") is None


def test_vector_cache_clear():
    cache = VectorCache(max_size=5)
    cache.put("a", np.array([1.0]))
    cache.clear()
    assert cache.size == 0
