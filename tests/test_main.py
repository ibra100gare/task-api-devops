from fastapi.testclient import TestClient

from app.main import app, tasks

client = TestClient(app)

def setup_function():
    tasks.clear()

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_list_task():
    response = client.post("/tasks", json={"title": "Apprendre Docker"})
    assert response.status_code == 201
    assert response.json()["title"] == "Apprendre Docker"
    assert client.get("/tasks").json()[0]["title"] == "Apprendre Docker"

def test_unknown_task_returns_404():
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_complete_task():
    created = client.post("/tasks", json={"title": "Configurer CI"})
    task_id = created.json()["id"]
    response = client.patch(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    assert response.json()["completed"] is True

def test_delete_task():
    created = client.post("/tasks", json={"title": "Supprimer"})
    task_id = created.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404
