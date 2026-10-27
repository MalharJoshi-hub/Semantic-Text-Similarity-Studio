"""Score calibration and distribution diagnostics."""

from typing import List, Dict, Any
import numpy as np


class ScoreCalibrator:
    """Computes distribution statistics (mean, variance, skew, quantiles) for similarity scores."""

    @staticmethod
    def analyze_distribution(scores: List[float]) -> Dict[str, float]:
        """Compute statistical properties of a collection of similarity scores."""
        arr = np.asarray(scores, dtype=np.float64)
        if len(arr) == 0:
            return {"count": 0, "mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0}

        return {
            "count": int(len(arr)),
            "mean": round(float(np.mean(arr)), 4),
            "std": round(float(np.std(arr)), 4),
            "min": round(float(np.min(arr)), 4),
            "max": round(float(np.max(arr)), 4),
            "p25": round(float(np.percentile(arr, 25)), 4),
            "median": round(float(np.median(arr)), 4),
            "p75": round(float(np.percentile(arr, 75)), 4),
            "p95": round(float(np.percentile(arr, 95)), 4),
        }
