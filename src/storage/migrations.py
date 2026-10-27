"""Database schema migrations and version tracking."""

import logging
from src.storage.database import DatabaseManager, get_db_manager

logger = logging.getLogger(__name__)


def run_migrations(db_manager: DatabaseManager = None):
    """Run database schema migrations sequentially."""
    db = db_manager or get_db_manager()
    with db.connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("SELECT MAX(version) FROM schema_version")
        row = cur.fetchone()
        current_version = row[0] if row and row[0] is not None else 0

        # Migration 1: Add section_title column to chunks if missing
        if current_version < 1:
            try:
                cur.execute("ALTER TABLE chunks ADD COLUMN section_title TEXT DEFAULT 'General'")
            except Exception:
                pass  # column may already exist
            cur.execute("INSERT INTO schema_version (version) VALUES (1)")
            conn.commit()
            logger.info("Applied migration 1: Added section_title to chunks table")
