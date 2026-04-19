from __future__ import annotations


class TestListTodos:
    def test_list_todos_empty_returns_empty_array(self, client):
        res = client.get("/api/todos/")

        assert res.status_code == 200
        assert res.json() == []

    def test_list_todos_returns_all_created_todos(self, client):
        client.post("/api/todos/", json={"title": "Task A"})
        client.post("/api/todos/", json={"title": "Task B"})

        res = client.get("/api/todos/")

        assert len(res.json()) == 2


class TestCreateTodo:
    def test_create_todo_returns_201(self, client):
        res = client.post("/api/todos/", json={"title": "Buy milk"})

        assert res.status_code == 201

    def test_create_todo_returns_correct_data(self, client):
        res = client.post("/api/todos/", json={"title": "Buy milk"})
        data = res.json()

        assert data["title"] == "Buy milk"
        assert data["done"] is False
        assert "id" in data
        assert "created_at" in data


class TestUpdateTodo:
    def test_update_todo_title_returns_updated_data(self, client):
        todo = client.post("/api/todos/", json={"title": "Old"}).json()

        res = client.put(f"/api/todos/{todo['id']}", json={"title": "New"})

        assert res.status_code == 200
        assert res.json()["title"] == "New"

    def test_update_todo_done_returns_updated_data(self, client):
        todo = client.post("/api/todos/", json={"title": "Task"}).json()

        res = client.put(f"/api/todos/{todo['id']}", json={"done": True})

        assert res.status_code == 200
        assert res.json()["done"] is True

    def test_update_todo_nonexistent_returns_404(self, client):
        res = client.put("/api/todos/999", json={"done": True})

        assert res.status_code == 404


class TestDeleteTodo:
    def test_delete_todo_returns_204(self, client):
        todo = client.post("/api/todos/", json={"title": "Delete me"}).json()

        res = client.delete(f"/api/todos/{todo['id']}")

        assert res.status_code == 204

    def test_delete_todo_removes_item(self, client):
        todo = client.post("/api/todos/", json={"title": "Delete me"}).json()
        client.delete(f"/api/todos/{todo['id']}")

        res = client.get("/api/todos/")
        assert res.json() == []

    def test_delete_todo_nonexistent_returns_404(self, client):
        res = client.delete("/api/todos/999")

        assert res.status_code == 404


class TestIndex:
    def test_index_returns_html(self, client):
        res = client.get("/")

        assert res.status_code == 200
        assert "text/html" in res.headers["content-type"]
