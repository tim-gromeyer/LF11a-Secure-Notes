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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY, 
            content TEXT, 
            user TEXT, 
            created_at TEXT, 
            tags TEXT
        )
    """)
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

from datetime import datetime
from typing import List, Optional

app = FastAPI(
    title="Secure Notes Enterprise API",
    description="Erweiterte sichere Notiz-Verwaltung mit Suche, Zeitstempeln und Multi-User-Support.",
    version="1.2.0"
)

# ... (security und get_db bleiben gleich)

class NoteCreate(BaseModel):
    content: str
    tags: Optional[str] = "Allgemein"

class Note(BaseModel):
    id: int
    content: str
    user: str
    created_at: str
    tags: Optional[str]

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('static/index.html')

@app.post("/notes", response_model=Note, tags=["Notizen"])
def create_note(note: NoteCreate, user: str = Depends(authenticate), db: sqlite3.Connection = Depends(get_db)):
    """Erstellt eine neue Notiz mit Zeitstempel und Tags."""
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO notes (content, user, created_at, tags) VALUES (?, ?, ?, ?)", 
        (note.content, user, created_at, note.tags)
    )
    db.commit()
    return {
        "id": cursor.lastrowid, 
        "content": note.content, 
        "user": user, 
        "created_at": created_at,
        "tags": note.tags
    }

@app.get("/notes", response_model=List[Note], tags=["Notizen"])
def get_notes(
    q: Optional[str] = None, 
    user: str = Depends(authenticate), 
    db: sqlite3.Connection = Depends(get_db)
):
    """Gibt Notizen zurück, optional gefiltert nach Suchbegriff 'q'."""
    cursor = db.cursor()
    if q:
        query = "SELECT id, content, user, created_at, tags FROM notes WHERE user = ? AND (content LIKE ? OR tags LIKE ?)"
        cursor.execute(query, (user, f"%{q}%", f"%{q}%"))
    else:
        query = "SELECT id, content, user, created_at, tags FROM notes WHERE user = ?"
        cursor.execute(query, (user,))
    
    return [
        {"id": row[0], "content": row[1], "user": row[2], "created_at": row[3], "tags": row[4]} 
        for row in cursor.fetchall()
    ]

@app.get("/stats", tags=["Administration"])
def get_stats(user: str = Depends(authenticate), db: sqlite3.Connection = Depends(get_db)):
    """Gibt Statistiken über die eigenen Notizen zurück."""
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM notes WHERE user = ?", (user,))
    count = cursor.fetchone()[0]
    return {"user": user, "total_notes": count, "system_status": "Secure"}

@app.delete("/notes/{note_id}", tags=["Notizen"])
def delete_note(note_id: int, user: str = Depends(authenticate), db: sqlite3.Connection = Depends(get_db)):
    """Löscht eine Notiz, sofern sie dem angemeldeten Benutzer gehört (Berechtigungsprüfung)."""
    cursor = db.cursor()
    # WICHTIG: Prüfung auf 'user', damit niemand fremde Notizen löscht!
    cursor.execute("DELETE FROM notes WHERE id = ? AND user = ?", (note_id, user))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden oder keine Berechtigung")
    db.commit()
    return {"status": "success", "message": f"Notiz {note_id} gelöscht"}

# Statische Dateien (Frontend) mounten
app.mount("/static", StaticFiles(directory="static"), name="static")