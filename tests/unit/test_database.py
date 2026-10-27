"""Unit tests for SQLite database manager and pragmas."""

import pytest


def test_database_init(test_db_manager):
    assert test_db_manager.db_path.exists()
    with test_db_manager.connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        assert "texts" in tables
        assert "chunks" in tables


def test_database_foreign_keys(test_db_manager):
    with test_db_manager.connection() as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA foreign_keys")
        fk_status = cur.fetchone()[0]
        assert fk_status == 1


def test_database_wal_mode(test_db_manager):
    with test_db_manager.connection() as conn:
        cur = conn.cursor()
        cur.execute("PRAGMA journal_mode")
        mode = cur.fetchone()[0]
        assert mode.lower() == "wal"
