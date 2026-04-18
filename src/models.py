from __future__ import annotations

from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None


class Todo(BaseModel):
    id: int
    title: str
    done: bool
    created_at: str
