"""Unit tests for ScoreCalibrator."""

import pytest
from src.benchmarks.calibration import ScoreCalibrator


def test_score_calibrator_empty():
    res = ScoreCalibrator.analyze_distribution([])
    assert res["count"] == 0
    assert res["mean"] == 0.0


def test_score_calibrator_distribution():
    scores = [0.1, 0.2, 0.5, 0.8, 0.9]
    res = ScoreCalibrator.analyze_distribution(scores)
    assert res["count"] == 5
    assert res["min"] == 0.1
    assert res["max"] == 0.9
    assert res["median"] == 0.5
    assert res["mean"] == 0.5
