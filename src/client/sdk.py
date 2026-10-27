"""Python SDK Client for interacting with the Semantic Similarity Studio REST API."""

from typing import Dict, Any, List, Optional
import requests


class SimilarityStudioClient:
    """Client for Semantic Similarity Studio REST API."""

    def __init__(self, base_url: str = "http://127.0.0.1:5000", timeout: float = 10.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def get_stats(self) -> Dict[str, Any]:
        """Fetch system statistics and vector corpus count."""
        resp = self.session.get(f"{self.base_url}/api/stats", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def compare(self, text1: str, text2: str) -> Dict[str, Any]:
        """Evaluate pairwise similarity between two texts."""
        payload = {"text1": text1, "text2": text2}
        resp = self.session.post(f"{self.base_url}/api/similarity", json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def list_corpus(self) -> List[Dict[str, Any]]:
        """List all indexed corpus documents."""
        resp = self.session.get(f"{self.base_url}/api/corpus", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json().get("texts", [])

    def ingest_text(self, label: str, content: str) -> Dict[str, Any]:
        """Ingest text document into corpus and FAISS vector index."""
        payload = {"label": label, "content": content}
        resp = self.session.post(f"{self.base_url}/api/corpus/text", json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search top-k most similar document chunks."""
        payload = {"query": query, "top_k": top_k}
        resp = self.session.post(f"{self.base_url}/api/search", json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def delete_document(self, doc_id: int) -> bool:
        """Delete document by ID."""
        resp = self.session.delete(f"{self.base_url}/api/corpus/{doc_id}", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json().get("success", False)

    def rebuild_index(self) -> Dict[str, Any]:
        """Trigger FAISS index reconstruction from SQLite database."""
        resp = self.session.post(f"{self.base_url}/api/rebuild", timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()
