from __future__ import annotations

import sqlite3

from fastapi import APIRouter, Depends, HTTPException

from src.database import DATABASE_URL, create_connection, init_db
from src.models import Todo, TodoCreate, TodoUpdate
from src.services import create_todo, delete_todo, get_all_todos, update_todo

router = APIRouter(prefix="/api/todos", tags=["todos"])


def get_db() -> sqlite3.Connection:
    conn = create_connection(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()


@router.get("/", response_model=list[Todo])
def list_todos(conn: sqlite3.Connection = Depends(get_db)):
    return get_all_todos(conn)


@router.post("/", response_model=Todo, status_code=201)
def add_todo(body: TodoCreate, conn: sqlite3.Connection = Depends(get_db)):
    return create_todo(conn, body.title)


@router.put("/{todo_id}", response_model=Todo)
def edit_todo(todo_id: int, body: TodoUpdate, conn: sqlite3.Connection = Depends(get_db)):
    result = update_todo(conn, todo_id, body)
    if result is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return result


@router.delete("/{todo_id}", status_code=204)
def remove_todo(todo_id: int, conn: sqlite3.Connection = Depends(get_db)):
    if not delete_todo(conn, todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
