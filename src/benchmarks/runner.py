"""Domain benchmark harness executing pairwise tests across domains."""

import time
from typing import Dict, Any, List
from src.core.embeddings import EmbeddingEngine, get_embedding_engine
from src.core.similarity import compute_cosine_similarity
from src.benchmarks.domains import ALL_DOMAINS


class DomainBenchmarkRunner:
    """Executes multi-domain test suites and computes accuracy, margin, and latency."""

    def __init__(self, embedder: EmbeddingEngine = None):
        self.embedder = embedder or get_embedding_engine()

    def run_benchmark(self) -> Dict[str, Any]:
        """Execute all domain benchmark tests."""
        start_time = time.perf_counter()
        domain_results = {}
        total_tests = 0
        passed_tests = 0

        for dom_key, dom_data in ALL_DOMAINS.items():
            tests_run = []
            dom_passed = 0
            for pair in dom_data["pairs"]:
                total_tests += 1
                t1 = pair["t1"]
                t2 = pair["t2"]

                v1 = self.embedder.encode(t1, normalize=True)
                v2 = self.embedder.encode(t2, normalize=True)
                score = compute_cosine_similarity(v1, v2)

                is_pass = True
                if "expected_min" in pair and score < pair["expected_min"]:
                    is_pass = False
                if "expected_max" in pair and score > pair["expected_max"]:
                    is_pass = False

                if is_pass:
                    passed_tests += 1
                    dom_passed += 1

                tests_run.append({
                    "label": pair["label"],
                    "score": round(score, 4),
                    "passed": is_pass,
                    "expected_min": pair.get("expected_min"),
                    "expected_max": pair.get("expected_max"),
                })

            domain_results[dom_key] = {
                "name": dom_data["name"],
                "total_pairs": len(dom_data["pairs"]),
                "passed_pairs": dom_passed,
                "accuracy": round(dom_passed / len(dom_data["pairs"]) * 100.0, 1),
                "tests": tests_run,
            }

        elapsed_sec = time.perf_counter() - start_time
        overall_accuracy = (passed_tests / total_tests * 100.0) if total_tests > 0 else 0.0

        return {
            "status": "success",
            "total_domains": len(ALL_DOMAINS),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "overall_accuracy_pct": round(overall_accuracy, 1),
            "execution_time_sec": round(elapsed_sec, 2),
            "domains": domain_results,
        }
