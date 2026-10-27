"""Unit tests for utility helpers (hashing, logger, telemetry)."""

import pytest
from src.utils.hashing import compute_text_hash
from src.utils.logger import setup_logger
from src.utils.telemetry import SystemTelemetry


def test_compute_text_hash():
    h1 = compute_text_hash("semantic similarity test")
    h2 = compute_text_hash("semantic similarity test")
    h3 = compute_text_hash("different text")

    assert len(h1) == 64
    assert h1 == h2
    assert h1 != h3


def test_setup_logger():
    log = setup_logger("test_logger")
    assert log.name == "test_logger"
    assert len(log.handlers) > 0


def test_system_telemetry():
    telemetry = SystemTelemetry()
    metrics = telemetry.get_metrics()
    assert "uptime_seconds" in metrics
    assert "pid" in metrics
    assert "memory" in metrics
