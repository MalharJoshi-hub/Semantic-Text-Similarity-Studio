"""Client SDK and Command-Line Interface for Semantic Similarity Studio."""

from src.client.sdk import SimilarityStudioClient
from src.client.cli import main as cli_main

__all__ = ["SimilarityStudioClient", "cli_main"]
