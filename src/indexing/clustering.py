"""K-Means clustering and vector centroid indexing."""

from typing import List, Dict, Any, Tuple
import numpy as np
from src.core.normalization import normalize_l2


class VectorClusterer:
    """Performs spherical K-Means clustering over normalized embeddings."""

    def __init__(self, n_clusters: int = 5, max_iter: int = 50, tolerance: float = 1e-4):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.tolerance = tolerance
        self.centroids: np.ndarray = np.empty((0, 0), dtype=np.float32)

    def fit(self, vectors: np.ndarray) -> np.ndarray:
        """Fit spherical k-means centroids on normalized vectors and return cluster assignments."""
        arr = normalize_l2(np.asarray(vectors, dtype=np.float32))
        n_samples, dim = arr.shape
        k = min(self.n_clusters, n_samples)

        if k <= 0:
            return np.empty(0, dtype=int)

        # Initialize centroids randomly from samples
        indices = np.random.choice(n_samples, size=k, replace=False)
        self.centroids = arr[indices].copy()

        labels = np.zeros(n_samples, dtype=int)
        for _ in range(self.max_iter):
            # Compute inner products between samples and centroids
            similarities = np.dot(arr, self.centroids.T)
            new_labels = np.argmax(similarities, axis=1)

            # Check convergence
            if np.array_equal(labels, new_labels):
                break
            labels = new_labels

            # Update centroids
            new_centroids = np.zeros_like(self.centroids)
            for c in range(k):
                mask = (labels == c)
                if np.any(mask):
                    cluster_mean = np.mean(arr[mask], axis=0)
                    new_centroids[c] = normalize_l2(cluster_mean)
                else:
                    new_centroids[c] = arr[np.random.choice(n_samples)]
            self.centroids = new_centroids

        return labels

    def predict(self, vectors: np.ndarray) -> np.ndarray:
        """Assign input vectors to nearest centroid."""
        if self.centroids.size == 0:
            raise ValueError("Clusterer has not been fitted yet.")
        arr = normalize_l2(np.asarray(vectors, dtype=np.float32))
        sims = np.dot(arr, self.centroids.T)
        return np.argmax(sims, axis=1)
