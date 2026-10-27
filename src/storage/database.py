"""SQLite database manager with WAL journaling, thread safety, and connection lifecycle."""

import os
import sqlite3
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

_LOCAL = threading.local()


class DatabaseManager:
    """Manages SQLite connections, pragmas, and schema initialization."""

    def __init__(self, db_path: str = "data/similarity.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_lock = threading.Lock()
        self.init_db()

    @contextmanager
    def connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Provide a contextual database connection configured with WAL and foreign keys."""
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        """Idempotently initialize tables and indices."""
        with self._init_lock:
            with self.connection() as conn:
                cur = conn.cursor()
                cur.execute("""
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
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS chunks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text_id INTEGER NOT NULL,
                        chunk_index INTEGER NOT NULL,
                        chunk_text TEXT NOT NULL,
                        char_count INTEGER NOT NULL,
                        word_count INTEGER NOT NULL,
                        section_title TEXT DEFAULT 'General',
                        FOREIGN KEY (text_id) REFERENCES texts(id) ON DELETE CASCADE
                    )
                """)
                cur.execute("CREATE INDEX IF NOT EXISTS idx_chunks_text_id ON chunks(text_id)")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_texts_created_at ON texts(created_at)")
                conn.commit()


_DB_MANAGER_INSTANCE = None
_DB_LOCK = threading.Lock()


def get_db_manager(db_path: str = "data/similarity.db") -> DatabaseManager:
    global _DB_MANAGER_INSTANCE
    if _DB_MANAGER_INSTANCE is None:
        with _DB_LOCK:
            if _DB_MANAGER_INSTANCE is None:
                _DB_MANAGER_INSTANCE = DatabaseManager(db_path)
    return _DB_MANAGER_INSTANCE
