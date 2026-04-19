from __future__ import annotations

from src.models import TodoUpdate
from src import services


class TestCreateTodo:
    def test_create_todo_with_valid_title_returns_todo(self, db):
        todo = services.create_todo(db, "Buy milk")

        assert todo.id is not None
        assert todo.title == "Buy milk"
        assert todo.done is False

    def test_create_todo_persists_in_db(self, db):
        services.create_todo(db, "Task 1")
        services.create_todo(db, "Task 2")

        todos = services.get_all_todos(db)
        assert len(todos) == 2


class TestGetAllTodos:
    def test_get_all_todos_empty_db_returns_empty_list(self, db):
        assert services.get_all_todos(db) == []

    def test_get_all_todos_returns_todos_in_insertion_order(self, db):
        services.create_todo(db, "First")
        services.create_todo(db, "Second")

        todos = services.get_all_todos(db)
        assert todos[0].title == "First"
        assert todos[1].title == "Second"


class TestUpdateTodo:
    def test_update_todo_title_changes_title(self, db):
        todo = services.create_todo(db, "Old title")

        updated = services.update_todo(db, todo.id, TodoUpdate(title="New title"))

        assert updated.title == "New title"

    def test_update_todo_done_marks_as_done(self, db):
        todo = services.create_todo(db, "Task")

        updated = services.update_todo(db, todo.id, TodoUpdate(done=True))

        assert updated.done is True

    def test_update_todo_partial_update_preserves_other_fields(self, db):
        todo = services.create_todo(db, "Keep this title")

        updated = services.update_todo(db, todo.id, TodoUpdate(done=True))

        assert updated.title == "Keep this title"
        assert updated.done is True

    def test_update_todo_nonexistent_returns_none(self, db):
        result = services.update_todo(db, 999, TodoUpdate(done=True))

        assert result is None


class TestDeleteTodo:
    def test_delete_todo_existing_returns_true(self, db):
        todo = services.create_todo(db, "Delete me")

        result = services.delete_todo(db, todo.id)

        assert result is True

    def test_delete_todo_removes_from_db(self, db):
        todo = services.create_todo(db, "Delete me")
        services.delete_todo(db, todo.id)

        assert services.get_all_todos(db) == []

    def test_delete_todo_nonexistent_returns_false(self, db):
        result = services.delete_todo(db, 999)

        assert result is False
