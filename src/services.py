from __future__ import annotations

import sqlite3

from src.models import Todo, TodoUpdate


def get_all_todos(conn: sqlite3.Connection) -> list[Todo]:
    rows = conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
    return [Todo(**dict(row)) for row in rows]


def create_todo(conn: sqlite3.Connection, title: str) -> Todo:
    cursor = conn.execute(
        "INSERT INTO todos (title, done) VALUES (?, 0)",
        (title,),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return Todo(**dict(row))


def update_todo(conn: sqlite3.Connection, todo_id: int, data: TodoUpdate) -> Todo | None:
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        return None
    new_title = data.title if data.title is not None else row["title"]
    new_done = int(data.done) if data.done is not None else row["done"]
    conn.execute(
        "UPDATE todos SET title = ?, done = ? WHERE id = ?",
        (new_title, new_done, todo_id),
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    return Todo(**dict(updated))


def delete_todo(conn: sqlite3.Connection, todo_id: int) -> bool:
    cursor = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    return cursor.rowcount > 0
