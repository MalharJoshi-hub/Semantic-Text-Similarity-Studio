"""Request and response schemas and payload validators."""

from typing import Dict, Any, Tuple, Optional


def validate_similarity_request(data: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """Validate payload for pairwise similarity endpoint."""
    if not isinstance(data, dict):
        return False, "Payload must be a valid JSON object."
    t1 = data.get("text1")
    t2 = data.get("text2")
    if not t1 or not isinstance(t1, str) or not t1.strip():
        return False, "Parameter 'text1' must be a non-empty string."
    if not t2 or not isinstance(t2, str) or not t2.strip():
        return False, "Parameter 'text2' must be a non-empty string."
    if len(t1) > 100000 or len(t2) > 100000:
        return False, "Text input exceeds maximum limit of 100,000 characters."
    return True, None


def validate_corpus_text_request(data: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """Validate payload for corpus text ingestion."""
    if not isinstance(data, dict):
        return False, "Payload must be a valid JSON object."
    label = data.get("label", "")
    content = data.get("content", "")
    if not content or not isinstance(content, str) or not content.strip():
        return False, "Parameter 'content' must be a non-empty string."
    if len(content) > 500000:
        return False, "Document content exceeds maximum limit of 500,000 characters."
    return True, None


def validate_search_request(data: Optional[Dict[str, Any]]) -> Tuple[bool, Optional[str]]:
    """Validate payload for corpus search."""
    if not isinstance(data, dict):
        return False, "Payload must be a valid JSON object."
    query = data.get("query")
    if not query or not isinstance(query, str) or not query.strip():
        return False, "Parameter 'query' must be a non-empty string."
    if len(query) > 5000:
        return False, "Query string exceeds maximum limit of 5,000 characters."
    return True, None
