"""Mathematical vector normalization and boundary precision helpers."""

from typing import Union
import numpy as np


def normalize_l2(vector: np.ndarray, epsilon: float = 1e-9) -> np.ndarray:
    """Normalize a 1D or 2D vector using strict L2 norm with numerical stability epsilon.

    Args:
        vector: NumPy array of shape (d,) or (n, d).
        epsilon: Minimum norm floor to prevent divide-by-zero.

    Returns:
        Normalized array with unit L2 norm along last axis.
    """
    arr = np.asarray(vector, dtype=np.float32)
    if arr.ndim == 1:
        norm = float(np.linalg.norm(arr))
        norm = max(norm, epsilon)
        return arr / norm
    elif arr.ndim == 2:
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        norms = np.maximum(norms, epsilon)
        return arr / norms
    else:
        raise ValueError(f"Expected 1D or 2D array, got shape {arr.shape}")


def clamp_score(score: Union[float, int, np.number], min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp float similarity scores strictly into interval [min_val, max_val].

    Args:
        score: Raw floating point or numpy scalar score.
        min_val: Lower bound (default: 0.0).
        max_val: Upper bound (default: 1.0).

    Returns:
        Float clamped strictly within bounds.
    """
    val = float(score)
    if np.isnan(val):
        return min_val
    if np.isneginf(val):
        return min_val
    if np.isposinf(val):
        return max_val
    return max(min_val, min(max_val, val))


def cosine_distance_to_similarity(distance: float) -> float:
    """Convert cosine distance (1 - cos) into cosine similarity cos."""
    return clamp_score(1.0 - distance)


def l2_distance_to_similarity(l2_dist: float) -> float:
    """Convert L2 distance between normalized vectors into bounded cosine similarity:
    ||u - v||^2 = 2 - 2*(u . v)  =>  (u . v) = 1 - 0.5 * ||u - v||^2
    """
    cos_sim = 1.0 - 0.5 * (l2_dist ** 2)
    return clamp_score(cos_sim)
