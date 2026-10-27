"""Command-line interface for Semantic Similarity Studio operations."""

import sys
import argparse
import json
from src.client.sdk import SimilarityStudioClient


def main():
    parser = argparse.ArgumentParser(description="Semantic Text Similarity & Retrieval Studio CLI")
    parser.add_argument("--url", default="http://127.0.0.1:5000", help="Base URL of Similarity Studio server")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # compare
    p_comp = subparsers.add_parser("compare", help="Compare two texts")
    p_comp.add_argument("--t1", required=True, help="First text string")
    p_comp.add_argument("--t2", required=True, help="Second text string")

    # search
    p_search = subparsers.add_parser("search", help="Search corpus by query")
    p_search.add_argument("--query", required=True, help="Search query string")
    p_search.add_argument("-k", "--top-k", type=int, default=5, help="Number of results")

    # ingest
    p_ingest = subparsers.add_parser("ingest", help="Ingest a document")
    p_ingest.add_argument("--label", required=True, help="Document title/label")
    p_ingest.add_argument("--file", required=True, help="Path to text or markdown file")

    # stats
    subparsers.add_parser("stats", help="Get corpus statistics")

    # rebuild
    subparsers.add_parser("rebuild", help="Rebuild FAISS index from SQLite")

    args = parser.parse_args()
    client = SimilarityStudioClient(base_url=args.url)

    try:
        if args.command == "compare":
            res = client.compare(args.t1, args.t2)
            print(f"Similarity: {res['percentage']}% ({res['tier']})")
            print(f"Cosine Score: {res['cosine_similarity']} | Lexical Overlap: {res['lexical_overlap']}")
        elif args.command == "search":
            results = client.search(args.query, top_k=args.top_k)
            print(f"Found {len(results)} matches for query: '{args.query}'\n")
            for idx, r in enumerate(results, 1):
                print(f"[{idx}] Score: {r['percentage']}% | Doc: {r['doc_label']} (Chunk #{r['chunk_index']})")
                print(f"    Snippet: {r['content'][:120]}...\n")
        elif args.command == "ingest":
            with open(args.file, "r", encoding="utf-8") as f:
                content = f.read()
            res = client.ingest_text(args.label, content)
            print(f"Successfully ingested '{args.label}' with {res.get('chunk_count', 0)} chunks.")
        elif args.command == "stats":
            stats = client.get_stats()
            print(json.dumps(stats, indent=2))
        elif args.command == "rebuild":
            res = client.rebuild_index()
            print(f"Index rebuild complete. Indexed chunks: {res.get('indexed_chunks', 0)}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
