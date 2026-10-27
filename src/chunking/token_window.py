"""Token-level sliding window chunker with exact word count control."""

from typing import List


class TokenWindowChunker:
    """Chunks arbitrary text into overlapping word token windows."""

    def __init__(self, window_size: int = 150, step_size: int = 120):
        if step_size <= 0:
            raise ValueError("step_size must be positive")
        self.window_size = window_size
        self.step_size = step_size

    def chunk(self, text: str) -> List[str]:
        """Split text into window_size token chunks with step_size stride."""
        words = text.split()
        if not words:
            return []
        if len(words) <= self.window_size:
            return [text.strip()]

        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.window_size, len(words))
            chunk_tokens = words[start:end]
            chunks.append(" ".join(chunk_tokens))
            if end >= len(words):
                break
            start += self.step_size

        return chunks
