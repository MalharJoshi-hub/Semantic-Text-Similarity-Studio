"""
Multi-Domain Benchmark Evaluation Harness for Semantic Similarity & FAISS Retrieval.
Executes against the running Semantic Studio API (http://127.0.0.1:5000).
Evaluates accuracy, score distributions, and retrieval latency across:
- Healthcare & Biomedicine
- Legal & Compliance
- Finance & FinTech
- Software Engineering & DevOps
"""

import time
import json
import urllib.request
import urllib.error
from datasets.domain_packs import DOMAIN_PACKS

BASE_URL = "http://127.0.0.1:5000"

def post_json(endpoint, payload):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def get_json(endpoint):
    req = urllib.request.Request(f"{BASE_URL}{endpoint}")
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))

def run_benchmark():
    print("=" * 80)
    print("  MULTI-DOMAIN SEMANTIC SIMILARITY & FAISS RETRIEVAL BENCHMARK")
    print(f"  Target Server: {BASE_URL} | Model: all-MiniLM-L6-v2 | FAISS: IndexFlatIP")
    print("=" * 80)

    # Check server health
    try:
        status, health = get_json("/api/stats")
        print(f"Server Status: {health.get('status')} | Model: {health.get('model')} (Dim: {health.get('embedding_dim')})")
    except Exception as e:
        print(f"ERROR: Could not connect to {BASE_URL}. Ensure 'python app.py' is running. Error: {e}")
        return

    overall_results = {}

    for domain_key, pack in DOMAIN_PACKS.items():
        print(f"\n>> Evaluating Domain: {pack['title'].upper()}")
        print("-" * 80)
        domain_report = {
            "title": pack["title"],
            "pairwise_tests": [],
            "retrieval_tests": []
        }

        # 1. Pairwise Semantic Similarity Tests
        print("  [1] Pairwise Semantic Similarity:")
        for preset in pack["presets"]:
            t1, t2 = preset["text1"], preset["text2"]
            status, res = post_json("/api/similarity/pair", {"text1": t1, "text2": t2})
            score = res["score"]
            pct = res["score_pct"]
            label = res["label"]

            print(f"      - {preset['name']:<30} -> Score: {score:.4f} ({pct:5.1f}%) | Tier: {label:<24} | Expected: {preset['expected']}")
            domain_report["pairwise_tests"].append({
                "test": preset["name"],
                "score": score,
                "percentage": pct,
                "label": label,
                "expected": preset["expected"]
            })

        # 2. Document Ingestion & Structural Chunking
        doc = pack["document"]
        status, ingest_res = post_json("/api/texts", {
            "label": f"[{pack['title']}] {doc['label']}",
            "content": doc["content"]
        })
        doc_record = ingest_res["document"]
        print(f"\n  [2] Ingestion & Indexing:")
        print(f"      - Document: '{doc_record['label']}'")
        print(f"      - Chunks generated: {doc_record['chunk_count']} | Words: {doc_record['word_count']}")

        # 3. Dense Vector Retrieval Tests
        print(f"\n  [3] FAISS Query Retrieval:")
        for q in pack["queries"]:
            t_start = time.perf_counter()
            status, q_res = post_json("/api/similarity/query", {"query": q, "top_k": 3})
            elapsed_ms = (time.perf_counter() - t_start) * 1000

            matches = q_res.get("results", [])
            if matches:
                top = matches[0]
                print(f"      - Query: \"{q}\"")
                print(f"        Rank #1 [{top['score_pct']}% Match | {top['label']}] in {elapsed_ms:.2f}ms")
                print(f"        Snippet: {top['snippet'][:80].replace(chr(10), ' ')}...")
                domain_report["retrieval_tests"].append({
                    "query": q,
                    "top_score": top["score"],
                    "top_pct": top["score_pct"],
                    "top_label": top["label"],
                    "latency_ms": round(elapsed_ms, 2),
                    "matched_doc": top["doc_label"]
                })
            else:
                print(f"      • Query: \"{q}\" -> No match found!")

        overall_results[domain_key] = domain_report

    # Summary Benchmark Table
    print("\n" + "=" * 80)
    print("  SUMMARY BENCHMARK MATRIX ACROSS 4 DOMAINS")
    print("=" * 80)
    print(f"{'Domain':<26} | {'Paraphrase':<12} | {'Contrasting':<12} | {'Cross-Unrelated':<15} | {'Search Top-1':<12}")
    print("-" * 80)

    for domain_key, report in overall_results.items():
        title = report["title"]
        pw = report["pairwise_tests"]
        rt = report["retrieval_tests"]

        para_score = f"{pw[0]['percentage']:.1f}%" if len(pw) > 0 else "N/A"
        contrast_score = f"{pw[2]['percentage']:.1f}%" if len(pw) > 2 else "N/A"
        unrel_score = f"{pw[3]['percentage']:.1f}%" if len(pw) > 3 else "N/A"
        avg_top1 = f"{sum(r['top_pct'] for r in rt) / len(rt):.1f}%" if rt else "N/A"

        print(f"{title:<26} | {para_score:<12} | {contrast_score:<12} | {unrel_score:<15} | {avg_top1:<12}")

    print("=" * 80)
    _, final_stats = get_json("/api/stats")
    print(f"Total Documents in Corpus: {final_stats['corpus']['total_texts']}")
    print(f"Total Chunks in FAISS Index: {final_stats['engine']['total_indexed_chunks']}")
    print("=" * 80)

    # Save summary report to JSON
    with open("data/benchmark_report.json", "w", encoding="utf-8") as f:
        json.dump(overall_results, f, indent=2)
    print("[OK] Full benchmark report saved to data/benchmark_report.json\n")

if __name__ == "__main__":
    run_benchmark()
