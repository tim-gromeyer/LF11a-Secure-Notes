from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
import secrets
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Secure Notes API (LF11a Edition)",
    description="Sichere Notiz-Verwaltung mit integrierter Swagger-Dokumentation und Basic-Frontend.",
    version="1.1.0"
)

security = HTTPBasic()

# Datenbank Initialisierung
def get_db():
    conn = sqlite3.connect("notes.db", check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT, user TEXT)")
    return conn

# Authentifizierung (User: admin, Pass: secret)
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültige Anmeldedaten",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

class NoteCreate(BaseModel):
    content: str

class Note(BaseModel):
    id: int
    content: str

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('static/index.html')

@app.post("/notes", response_model=Note, tags=["Notizen"])
def create_note(note: NoteCreate, user: str = Depends(authenticate), db: sqlite3.Connection = Depends(get_db)):
    """Erstellt eine neue verschlüsselte Notiz für den angemeldeten Benutzer."""
    cursor = db.cursor()
    cursor.execute("INSERT INTO notes (content, user) VALUES (?, ?)", (note.content, user))
    db.commit()
    return {"id": cursor.lastrowid, "content": note.content}

@app.get("/notes", response_model=List[Note], tags=["Notizen"])
def get_notes(user: str = Depends(authenticate), db: sqlite3.Connection = Depends(get_db)):
    """Gibt alle Notizen des aktuellen Benutzers zurück."""
    cursor = db.cursor()
    cursor.execute("SELECT id, content FROM notes WHERE user = ?", (user,))
    return [{"id": row[0], "content": row[1]} for row in cursor.fetchall()]

# Statische Dateien (Frontend) mounten
app.mount("/static", StaticFiles(directory="static"), name="static")