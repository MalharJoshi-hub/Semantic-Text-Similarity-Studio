"""Pytest configuration and shared test fixtures."""

import os
import tempfile
import pytest
import numpy as np

from src.storage.database import DatabaseManager
from src.storage.repositories import TextRepository, ChunkRepository
from src.indexing.faiss_engine import FaissIndexEngine
from src.core.embeddings import EmbeddingEngine


@pytest.fixture
def temp_dir():
    """Provides a temporary directory that is automatically cleaned up."""
    with tempfile.TemporaryDirectory() as tmp:
        yield tmp


@pytest.fixture
def test_db_manager(temp_dir):
    """Provides an isolated SQLite DatabaseManager in a temporary directory."""
    db_path = os.path.join(temp_dir, "test_similarity.db")
    return DatabaseManager(db_path=db_path)


@pytest.fixture
def test_text_repo(test_db_manager):
    """Provides an isolated TextRepository."""
    return TextRepository(db_manager=test_db_manager)


@pytest.fixture
def test_chunk_repo(test_db_manager):
    """Provides an isolated ChunkRepository."""
    return ChunkRepository(db_manager=test_db_manager)


@pytest.fixture
def test_faiss_engine(temp_dir):
    """Provides an isolated FaissIndexEngine in a temporary directory."""
    idx_path = os.path.join(temp_dir, "test.index")
    meta_path = os.path.join(temp_dir, "test_meta.pkl")
    return FaissIndexEngine(dimension=384, index_file=idx_path, meta_file=meta_path)


@pytest.fixture
def sample_vectors():
    """Generates deterministic pseudo-random unit vectors for math testing."""
    np.random.seed(42)
    vecs = np.random.randn(10, 384).astype(np.float32)
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    return vecs / norms


@pytest.fixture
def flask_test_client():
    """Provides a test client for the main Flask application."""
    from app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
