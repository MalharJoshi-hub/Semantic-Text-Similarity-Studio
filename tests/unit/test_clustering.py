"""Unit tests for spherical VectorClusterer."""

import pytest
import numpy as np
from src.indexing.clustering import VectorClusterer


def test_vector_clusterer_fit_predict():
    clusterer = VectorClusterer(n_clusters=3, max_iter=20)
    vectors = np.random.randn(30, 64).astype(np.float32)

    labels = clusterer.fit(vectors)
    assert len(labels) == 30
    assert set(labels).issubset({0, 1, 2})
    assert clusterer.centroids.shape == (3, 64)

    # Predict on new vectors
    new_vecs = np.random.randn(5, 64).astype(np.float32)
    preds = clusterer.predict(new_vecs)
    assert len(preds) == 5
    assert set(preds).issubset({0, 1, 2})
