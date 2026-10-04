"""
Database Module for Semantic Text Similarity System.
Manages texts and their structural chunks in SQLite with robust connection pooling/handling.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "similarity.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Initializes the database schema."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                label TEXT NOT NULL,
                content TEXT NOT NULL,
                source_type TEXT DEFAULT 'text',
                char_count INTEGER NOT NULL,
                word_count INTEGER NOT NULL,
                chunk_count INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_id INTEGER NOT NULL,
                chunk_index INTEGER NOT NULL,
                chunk_text TEXT NOT NULL,
                char_count INTEGER NOT NULL,
                word_count INTEGER NOT NULL,
                FOREIGN KEY (text_id) REFERENCES texts(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

def add_text(label: str, content: str, chunks: List[str], source_type: str = "text") -> Dict[str, Any]:
    """Adds a text document and its chunks into SQLite."""
    content = content.strip()
    label = label.strip() or "Untitled Document"
    char_count = len(content)
    word_count = len(content.split())
    chunk_count = len(chunks)
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO texts (label, content, source_type, char_count, word_count, chunk_count, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (label, content, source_type, char_count, word_count, chunk_count, created_at))
        text_id = cur.lastrowid

        chunk_rows = []
        for idx, chunk in enumerate(chunks):
            c_char = len(chunk)
            c_word = len(chunk.split())
            chunk_rows.append((text_id, idx, chunk, c_char, c_word))

        cur.executemany("""
            INSERT INTO chunks (text_id, chunk_index, chunk_text, char_count, word_count)
            VALUES (?, ?, ?, ?, ?)
        """, chunk_rows)
        conn.commit()

    return {
        "id": text_id,
        "label": label,
        "source_type": source_type,
        "char_count": char_count,
        "word_count": word_count,
        "chunk_count": chunk_count,
        "created_at": created_at
    }

def get_texts() -> List[Dict[str, Any]]:
    """Returns a list of all stored texts with metadata."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, label, source_type, char_count, word_count, chunk_count, created_at
            FROM texts
            ORDER BY id DESC
        """)
        rows = cur.fetchall()
        return [dict(r) for r in rows]

def get_text(text_id: int) -> Optional[Dict[str, Any]]:
    """Returns a specific text by ID including its chunks."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, label, content, source_type, char_count, word_count, chunk_count, created_at
            FROM texts WHERE id = ?
        """, (text_id,))
        row = cur.fetchone()
        if not row:
            return None

        doc = dict(row)
        cur.execute("""
            SELECT id, chunk_index, chunk_text, char_count, word_count
            FROM chunks WHERE text_id = ?
            ORDER BY chunk_index ASC
        """, (text_id,))
        doc["chunks"] = [dict(c) for c in cur.fetchall()]
        return doc

def delete_text(text_id: int) -> bool:
    """Deletes a text and its cascaded chunks."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM texts WHERE id = ?", (text_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        return deleted

def get_all_chunks() -> List[Dict[str, Any]]:
    """Fetches all chunks across all texts with document labels for FAISS index rebuild."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id as chunk_id, c.text_id, t.label as doc_label, c.chunk_index, c.chunk_text
            FROM chunks c
            JOIN texts t ON c.text_id = t.id
            ORDER BY c.text_id ASC, c.chunk_index ASC
        """)
        rows = cur.fetchall()
        return [dict(r) for r in rows]

def get_db_stats() -> Dict[str, Any]:
    """Returns corpus statistics."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM texts")
        total_texts = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM chunks")
        total_chunks = cur.fetchone()[0]
        cur.execute("SELECT COALESCE(SUM(word_count), 0) FROM texts")
        total_words = cur.fetchone()[0]
        return {
            "total_texts": total_texts,
            "total_chunks": total_chunks,
            "total_words": total_words
        }

def clear_all():
    """Clears all texts and chunks from the database."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM chunks")
        cur.execute("DELETE FROM texts")
        conn.commit()
