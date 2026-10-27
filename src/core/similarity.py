"""Pairwise semantic and lexical similarity calculations."""

import re
import time
from typing import Set, Tuple, List
import numpy as np

from src.core.normalization import normalize_l2, clamp_score
from src.core.types import SimilarityResult, TierInfo

# Standard stopwords for lexical overlap filtering
STOPWORDS: Set[str] = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves"
}

TIERS: List[TierInfo] = [
    TierInfo("Extremely High Similarity", "#10b981", "Identical sentences, direct paraphrases, or synonymous phrasing.", 0.85, 1.00),
    TierInfo("High Semantic Similarity", "#34d399", "Strong contextual and conceptual overlap with shared core themes.", 0.70, 0.85),
    TierInfo("Moderate Semantic Overlap", "#f59e0b", "Shared domain or topical overlap, but divergence in specific focus.", 0.50, 0.70),
    TierInfo("Low / Weak Relevance", "#fb923c", "Minor connection or isolated technical terms; overall intent differs.", 0.30, 0.50),
    TierInfo("Unrelated / Distinct", "#94a3b8", "Completely unrelated domains or topics with no conceptual linkage.", 0.00, 0.30),
]


def classify_similarity_tier(score: float) -> Tuple[str, str, str]:
    """Map a similarity score [0.0, 1.0] to tier name, color, and description."""
    s = clamp_score(score)
    for tier in TIERS:
        if s >= tier.threshold_min:
            return tier.tier, tier.color, tier.description
    return TIERS[-1].tier, TIERS[-1].color, TIERS[-1].description


def tokenize_clean(text: str) -> List[str]:
    """Extract lowercased alphanumeric tokens from text."""
    if not text:
        return []
    return re.findall(r"\b[a-zA-Z0-9_\-']+\b", text.lower())


def compute_lexical_jaccard(text1: str, text2: str, remove_stopwords: bool = True) -> float:
    """Compute Jaccard similarity index on token sets.

    J(A, B) = |A ∩ B| / |A ∪ B|
    """
    tokens1 = tokenize_clean(text1)
    tokens2 = tokenize_clean(text2)

    if remove_stopwords:
        set1 = {t for t in tokens1 if t not in STOPWORDS}
        set2 = {t for t in tokens2 if t not in STOPWORDS}
    else:
        set1 = set(tokens1)
        set2 = set(tokens2)

    if not set1 and not set2:
        return 1.0 if not tokens1 and not tokens2 else 0.0
    if not set1 or not set2:
        return 0.0

    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return float(intersection) / float(union) if union > 0 else 0.0


def compute_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors using normalized dot product."""
    u = normalize_l2(vec1)
    v = normalize_l2(vec2)
    raw = float(np.dot(u, v))
    return clamp_score(raw)


def evaluate_pairwise_similarity(
    text1: str,
    text2: str,
    vec1: np.ndarray,
    vec2: np.ndarray,
    start_time: float,
) -> SimilarityResult:
    """Assemble complete SimilarityResult contract from texts and embeddings."""
    cosine_sim = compute_cosine_similarity(vec1, vec2)
    percentage = cosine_sim * 100.0
    lexical = compute_lexical_jaccard(text1, text2)
    tier_name, tier_color, tier_desc = classify_similarity_tier(cosine_sim)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    return SimilarityResult(
        cosine_similarity=cosine_sim,
        percentage=percentage,
        lexical_overlap=lexical,
        tier=tier_name,
        color=tier_color,
        tier_description=tier_desc,
        text1_word_count=len(text1.split()),
        text2_word_count=len(text2.split()),
        text1_char_count=len(text1),
        text2_char_count=len(text2),
        computation_time_ms=elapsed_ms,
        vector_dimension=int(len(vec1)),
    )
