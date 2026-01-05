import os
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Remove old db if exists to start fresh
if os.path.exists("notes.db"):
    os.remove("notes.db")

def test_read_main_unauthorized():
    response = client.get("/notes")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_create_note():
    response = client.post(
        "/notes",
        json={"content": "Geheime Notiz 1"},
        auth=("admin", "secret")
    )
    assert response.status_code == 200
    assert response.json()["content"] == "Geheime Notiz 1"

def test_read_notes():
    response = client.get("/notes", auth=("admin", "secret"))
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["content"] == "Geheime Notiz 1"