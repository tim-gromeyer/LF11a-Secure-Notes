import sqlite3
import secrets
import hashlib
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="Secure Notes Enterprise API",
    description="Sichere Notiz-Verwaltung mit Suche, Zeitstempeln und Multi-User-Support für LF11a.",
    version="1.3.0"
)

security = HTTPBasic()

# Passwort für 'admin' ist 'secret'.
# Hier simulieren wir eine Benutzer-DB mit Salted SHA-256 Hashes.
# In einer Produktiv-Umgebung käme dies aus einer DB-Tabelle 'users'.
USER_DB = {
    "admin": {
        "salt": "lf11a_salt_demo",
        "hashed_password": hashlib.sha256(("secret" + "lf11a_salt_demo").encode()).hexdigest()
    }
}

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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user TEXT,
            expires_at DATETIME
        )
    """)
    return conn

# Neue Authentifizierungs-Logik (Session-Tokens statt Basic Auth)
from fastapi.security import APIKeyHeader
session_scheme = APIKeyHeader(name="X-Session-Token")

def authenticate(token: str = Depends(session_scheme), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT user FROM sessions WHERE token = ?", (token,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session abgelaufen oder ungültig",
        )
    return row[0]

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login", tags=["Auth"])
def login(auth: LoginRequest, db: sqlite3.Connection = Depends(get_db)):
    user_record = USER_DB.get(auth.username)
    if not user_record:
        raise HTTPException(status_code=401, detail="Falsche Anmeldedaten")
    
    input_hash = hashlib.sha256((auth.password + user_record["salt"]).encode()).hexdigest()
    if not secrets.compare_digest(input_hash, user_record["hashed_password"]):
        raise HTTPException(status_code=401, detail="Falsche Anmeldedaten")
    
    # Session Token generieren (sichere Zufallsfolge)
    token = secrets.token_urlsafe(32)
    cursor = db.cursor()
    cursor.execute("INSERT INTO sessions (token, user) VALUES (?, ?)", (token, auth.username))
    db.commit()
    return {"token": token, "user": auth.username}

@app.post("/logout", tags=["Auth"])
def logout(token: str = Depends(session_scheme), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    db.commit()
    return {"message": "Abgemeldet"}

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
    created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
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
    """Löscht eine Notiz, sofern sie dem angemeldeten Benutzer gehört."""
    cursor = db.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ? AND user = ?", (note_id, user))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden oder keine Berechtigung")
    db.commit()
    return {"status": "success", "message": f"Notiz {note_id} gelöscht"}

# Statische Dateien mounten
app.mount("/static", StaticFiles(directory="static"), name="static")