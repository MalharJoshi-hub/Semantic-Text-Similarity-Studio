"""Integration tests evaluating domain benchmark accuracy."""

import pytest
from src.benchmarks.runner import DomainBenchmarkRunner


def test_domain_benchmark_suite():
    runner = DomainBenchmarkRunner()
    res = runner.run_benchmark()
    assert res["status"] == "success"
    assert res["total_domains"] >= 10
    assert res["overall_accuracy_pct"] >= 75.0
    assert res["passed_tests"] > 0
