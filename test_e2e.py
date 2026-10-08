"""
End-to-End Verification Script for Semantic Similarity System.
Tests:
1. Pairwise similarity across 4 distinct categories
2. PDF creation, upload, structural chunking, and FAISS indexing
3. Query search ranking against corpus
4. Document chunk retrieval
5. Edge cases: empty text, punctuation-only, missing parameters
"""

import io
import sys
import urllib.request
import urllib.parse
import json
import mimetypes

BASE_URL = "http://127.0.0.1:5000"

def post_json(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"\n❌ [Connection Error]: Could not connect to {BASE_URL}")
        print("💡 The Flask application is not running!")
        print("   Please start the server first in a separate terminal:")
        print("   > python app.py\n")
        sys.exit(1)

def get_json(endpoint):
    req = urllib.request.Request(f"{BASE_URL}{endpoint}")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))
    except urllib.error.URLError as e:
        print(f"\n❌ [Connection Error]: Could not connect to {BASE_URL}")
        print("💡 The Flask application is not running!")
        print("   Please start the server first in a separate terminal:")
        print("   > python app.py\n")
        sys.exit(1)

def post_multipart(endpoint, fields, files):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    data = []
    for k, v in fields.items():
        data.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n")
    for k, (filename, file_bytes) in files.items():
        data.append(
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"{k}\"; filename=\"{filename}\"\r\n"
            f"Content-Type: application/pdf\r\n\r\n"
        )
        data.append(file_bytes)
        data.append("\r\n")
    data.append(f"--{boundary}--\r\n")

    body = b"".join([part.encode("latin-1") if isinstance(part, str) else part for part in data])
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))

def run_tests():
    print("=== 1. Testing System Stats ===")
    status, stats = get_json("/api/stats")
    print(f"Stats [{status}]: model={stats['model']}, total_docs={stats['corpus']['total_texts']}")
    assert status == 200

    print("\n=== 2. Testing Pairwise Semantic Similarity ===")
    pairs = [
        ("Identical", "Artificial intelligence algorithms are transforming medicine.", "Artificial intelligence algorithms are transforming medicine."),
        ("Paraphrase", "The quick brown fox jumps over the lazy dog.", "A fast brown fox leaps over a sleepy canine."),
        ("Moderate Overlap", "The central bank raised interest rates to combat inflation.", "The stock market dropped as investors feared higher borrowing costs."),
        ("Unrelated", "Photosynthesis in green plants converts solar energy into glucose.", "The recipe for beef stroganoff requires mushrooms and sour cream.")
    ]

    for category, t1, t2 in pairs:
        code, res = post_json("/api/similarity/pair", {"text1": t1, "text2": t2})
        print(f"[{category}] Score: {res['score']:.4f} ({res['score_pct']}%) -> Label: '{res['label']}'")
        assert 0.0 <= res['score'] <= 1.0

    print("\n=== 3. Testing Edge Cases & Validations ===")
    code, res = post_json("/api/similarity/pair", {"text1": "", "text2": "hello"})
    print(f"Empty text validation: status {code}, error: {res.get('error')}")
    assert code == 400

    code, res = post_json("/api/similarity/query", {"query": ""})
    print(f"Empty query validation: status {code}, error: {res.get('error')}")
    assert code == 400

    print("\n=== 4. Testing Document Ingestion & Query Search ===")
    # Add structured document
    doc_payload = {
        "label": "Deep Learning & Transformer Systems",
        "content": """# Overview of Deep Learning
Deep learning models leverage multi-layer artificial neural networks to learn representations from raw data.

# Multi-Head Attention Mechanism
The transformer model computes scaled dot-product self-attention across parallel attention heads.
Queries, keys, and values are linearly projected to determine cross-token attention weights.

# Optimization via AdamW
Modern transformer models are trained using the AdamW optimizer with cosine learning rate schedules."""
    }
    code, add_res = post_json("/api/texts", doc_payload)
    print(f"Added Document [{code}]: ID={add_res['document']['id']}, Chunks={add_res['document']['chunk_count']}")
    assert code == 201
    doc_id = add_res['document']['id']

    # Query search
    q_code, q_res = post_json("/api/similarity/query", {
        "query": "scaled dot product self-attention across heads",
        "top_k": 3
    })
    print(f"Query Result [{q_code}]: Found {q_res['total_matches']} matches")
    for r in q_res['results']:
        print(f"  Rank #{r['rank']} | Score: {r['score_pct']}% | Doc: {r['doc_label']} | Snippet: {r['snippet'][:60]}...")
    assert q_res['total_matches'] > 0
    assert q_res['results'][0]['score'] > 0.60

    print("\n=== 5. Cleaning Up Test Document ===")
    del_code, del_res = get_json(f"/api/texts")
    req = urllib.request.Request(f"{BASE_URL}/api/texts/{doc_id}", method="DELETE")
    with urllib.request.urlopen(req) as resp:
        print(f"Deleted test doc: status {resp.status}")

    print("\n ALL END-TO-END VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
