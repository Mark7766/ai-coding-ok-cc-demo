from __future__ import annotations

import os
import sqlite3

DATABASE_URL = os.getenv("DATABASE_URL", "demo.db")

_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS todos (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        title      TEXT    NOT NULL,
        done       INTEGER NOT NULL DEFAULT 0,
        created_at TEXT    NOT NULL DEFAULT (datetime('now'))
    )
"""


def create_connection(database_url: str = DATABASE_URL) -> sqlite3.Connection:
    conn = sqlite3.connect(database_url, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(_CREATE_TABLE)
    conn.commit()
