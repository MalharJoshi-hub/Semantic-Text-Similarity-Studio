"""Repository implementations for documents and structural chunks."""

from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from src.storage.database import DatabaseManager, get_db_manager
from src.storage.models import TextRecord, ChunkRecord, CorpusStats


class TextRepository:
    """Data access repository for parent document texts."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or get_db_manager()

    def add_text(self, label: str, content: str, chunks: List[str], source_type: str = "text") -> TextRecord:
        """Persist a new document and all its chunks atomically."""
        clean_content = content.strip()
        clean_label = label.strip() or "Untitled Document"
        char_count = len(clean_content)
        word_count = len(clean_content.split())
        chunk_count = len(chunks)
        created_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        with self.db.connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO texts (label, content, source_type, char_count, word_count, chunk_count, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (clean_label, clean_content, source_type, char_count, word_count, chunk_count, created_at))
            text_id = cur.lastrowid

            chunk_rows = []
            for idx, c_text in enumerate(chunks):
                chunk_rows.append((text_id, idx, c_text, len(c_text), len(c_text.split()), "General"))

            cur.executemany("""
                INSERT INTO chunks (text_id, chunk_index, chunk_text, char_count, word_count, section_title)
                VALUES (?, ?, ?, ?, ?, ?)
            """, chunk_rows)
            conn.commit()

        record = TextRecord(
            id=text_id,
            label=clean_label,
            content=clean_content,
            source_type=source_type,
            char_count=char_count,
            word_count=word_count,
            chunk_count=chunk_count,
            created_at=created_at,
        )
        return record

    def list_all(self) -> List[TextRecord]:
        """Fetch all documents ordered descending by creation date."""
        with self.db.connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, label, content, source_type, char_count, word_count, chunk_count, created_at
                FROM texts
                ORDER BY id DESC
            """)
            rows = cur.fetchall()
            return [
                TextRecord(
                    id=r["id"],
                    label=r["label"],
                    content=r["content"],
                    source_type=r["source_type"],
                    char_count=r["char_count"],
                    word_count=r["word_count"],
                    chunk_count=r["chunk_count"],
                    created_at=r["created_at"],
                )
                for r in rows
            ]

    def get_by_id(self, text_id: int) -> Optional[TextRecord]:
        """Fetch document by primary key including all its associated chunks."""
        with self.db.connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, label, content, source_type, char_count, word_count, chunk_count, created_at
                FROM texts WHERE id = ?
            """, (text_id,))
            row = cur.fetchone()
            if not row:
                return None

            cur.execute("""
                SELECT id, text_id, chunk_index, chunk_text, char_count, word_count, section_title
                FROM chunks WHERE text_id = ?
                ORDER BY chunk_index ASC
            """, (text_id,))
            chunk_rows = cur.fetchall()

            chunks = [
                ChunkRecord(
                    id=c["id"],
                    text_id=c["text_id"],
                    chunk_index=c["chunk_index"],
                    chunk_text=c["chunk_text"],
                    char_count=c["char_count"],
                    word_count=c["word_count"],
                    section_title=c["section_title"],
                )
                for c in chunk_rows
            ]

            return TextRecord(
                id=row["id"],
                label=row["label"],
                content=row["content"],
                source_type=row["source_type"],
                char_count=row["char_count"],
                word_count=row["word_count"],
                chunk_count=row["chunk_count"],
                created_at=row["created_at"],
                chunks=chunks,
            )

    def delete(self, text_id: int) -> bool:
        """Delete document and rely on SQLite CASCADE to delete its chunks."""
        with self.db.connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM texts WHERE id = ?", (text_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted

    def get_stats(self) -> CorpusStats:
        """Compute aggregated corpus stats."""
        with self.db.connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM texts")
            total_texts = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM chunks")
            total_chunks = cur.fetchone()[0]
            cur.execute("SELECT COALESCE(SUM(word_count), 0) FROM texts")
            total_words = cur.fetchone()[0]
            return CorpusStats(total_texts=total_texts, total_chunks=total_chunks, total_words=total_words)

    def clear(self):
        """Purge all text and chunk records."""
        with self.db.connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM chunks")
            cur.execute("DELETE FROM texts")
            conn.commit()


class ChunkRepository:
    """Data access repository for individual chunks."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db = db_manager or get_db_manager()

    def get_all_for_rebuild(self) -> List[Dict[str, Any]]:
        """Fetch all chunks joined with parent text label for index reconstruction."""
        with self.db.connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT c.id as chunk_id, c.text_id, t.label as doc_label, c.chunk_index, c.chunk_text, c.section_title, c.word_count
                FROM chunks c
                JOIN texts t ON c.text_id = t.id
                ORDER BY c.text_id ASC, c.chunk_index ASC
            """)
            rows = cur.fetchall()
            return [
                {
                    "id": r["chunk_id"],
                    "text_id": r["text_id"],
                    "doc_id": r["text_id"],
                    "doc_title": r["doc_label"],
                    "doc_label": r["doc_label"],
                    "chunk_index": r["chunk_index"],
                    "chunk_text": r["chunk_text"],
                    "content": r["chunk_text"],
                    "section_title": r["section_title"] or "General",
                    "word_count": r["word_count"],
                }
                for r in rows
            ]
