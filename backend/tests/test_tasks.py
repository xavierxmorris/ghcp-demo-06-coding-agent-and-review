from fastapi.testclient import TestClient
from app.main import app, store

client = TestClient(app)


def setup_function(_):
    store._items.clear()


def test_create_and_list_task():
    r = client.post("/tasks", json={"title": "demo"})
    assert r.status_code == 201
    task = r.json()
    assert task["title"] == "demo"
    assert task["done"] is False

    r = client.get("/tasks")
    assert r.status_code == 200
    assert len(r.json()) == 1


def test_update_unknown_task_returns_404():
    r = client.patch("/tasks/does-not-exist", json={"done": True})
    assert r.status_code == 404
