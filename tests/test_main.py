import os
import pytest
import sqlite3
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

# Verwende eine In-Memory-Datenbank fuer die Tests, um die lokale notes.db nicht zu loeschen
def override_get_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    # Schema initialisieren
    conn.execute("CREATE TABLE users (username TEXT PRIMARY KEY, hashed_password TEXT, salt TEXT)")
    conn.execute("CREATE TABLE sessions (token TEXT PRIMARY KEY, user TEXT, expires_at DATETIME)")
    conn.execute("CREATE TABLE notes (id INTEGER PRIMARY KEY, title TEXT, content TEXT, user TEXT, created_at TEXT, tags TEXT)")
    conn.execute("CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, timestamp TEXT, user TEXT, action TEXT, resource_id INTEGER, details TEXT)")
    return conn

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_registration_and_login():
    # 1. Benutzer registrieren
    reg_res = client.post("/register", json={"username": "testuser", "password": "testpassword"})
    assert reg_res.status_code == 200
    
    # 2. Login
    login_res = client.post("/login", json={"username": "testuser", "password": "testpassword"})
    assert login_res.status_code == 200
    token = login_res.json()["token"]
    assert token is not None
    return token

def test_unauthorized_access():
    response = client.get("/notes")
    assert response.status_code == 401

def test_note_lifecycle():
    token = test_registration_and_login()
    headers = {"X-Session-Token": token}
    
    # Create
    create_res = client.post("/notes", json={"title": "Test", "content": "Test Content", "tags": "Test"}, headers=headers)
    assert create_res.status_code == 200
    note_id = create_res.json()["id"]
    
    # Read
    get_res = client.get("/notes", headers=headers)
    assert len(get_res.json()) == 1
    assert get_res.json()[0]["title"] == "Test"
    
    # Update
    update_res = client.put(f"/notes/{note_id}", json={"title": "Updated", "content": "New Content", "tags": "Updated"}, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "Updated"
    
    # Delete
    del_res = client.delete(f"/notes/{note_id}", headers=headers)
    assert del_res.status_code == 200
    
    # Verify deletion
    final_res = client.get("/notes", headers=headers)
    assert len(final_res.json()) == 0

def test_admin_access_restriction():
    token = test_registration_and_login() # Normaler User
    headers = {"X-Session-Token": token}
    
    response = client.get("/admin/logs", headers=headers)
    assert response.status_code == 403

def test_search_functionality():
    token = test_registration_and_login()
    headers = {"X-Session-Token": token}
    
    client.post("/notes", json={"title": "Pizza", "content": "Salami", "tags": "Essen"}, headers=headers)
    client.post("/notes", json={"title": "Pasta", "content": "Carbonara", "tags": "Essen"}, headers=headers)
    
    # Suche nach Pizza
    search_res = client.get("/notes?q=Pizza", headers=headers)
    assert len(search_res.json()) == 1
    assert search_res.json()[0]["title"] == "Pizza"
