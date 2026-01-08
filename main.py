import secrets
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Lokale Importe
from database import get_db
from models import NoteCreate, Note, LoginRequest
from auth import get_current_user, verify_password, session_scheme

app = FastAPI(
    title="Secure Notes Enterprise API",
    description="Modularisierte sichere Notiz-Verwaltung für LF11a.",
    version="2.1.0"
)

@app.get("/", include_in_schema=False)
async def read_index():
    return FileResponse('static/index.html')

@app.post("/login", tags=["Auth"])
def login(auth: LoginRequest, db=Depends(get_db)):
    if not verify_password(auth.password, auth.username):
        raise HTTPException(status_code=401, detail="Falsche Anmeldedaten")
    
    token = secrets.token_urlsafe(32)
    cursor = db.cursor()
    cursor.execute("INSERT INTO sessions (token, user) VALUES (?, ?)", (token, auth.username))
    db.commit()
    return {"token": token, "user": auth.username}

@app.post("/logout", tags=["Auth"])
def logout(token: str = Depends(session_scheme), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    db.commit()
    return {"message": "Abgemeldet"}

@app.post("/notes", response_model=Note, tags=["Notizen"])
def create_note(note: NoteCreate, user: str = Depends(get_current_user), db=Depends(get_db)):
    created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO notes (title, content, user, created_at, tags) VALUES (?, ?, ?, ?, ?)", 
        (note.title, note.content, user, created_at, note.tags)
    )
    db.commit()
    return {
        "id": cursor.lastrowid, 
        "title": note.title,
        "content": note.content, 
        "user": user, 
        "created_at": created_at,
        "tags": note.tags
    }

@app.get("/notes", response_model=List[Note], tags=["Notizen"])
def get_notes(
    q: Optional[str] = None, 
    user: str = Depends(get_current_user), 
    db=Depends(get_db)
):
    cursor = db.cursor()
    if q:
        query = "SELECT id, title, content, user, created_at, tags FROM notes WHERE user = ? AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)"
        cursor.execute(query, (user, f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("SELECT id, title, content, user, created_at, tags FROM notes WHERE user = ?", (user,))
    
    return [
        {"id": row[0], "title": row[1], "content": row[2], "user": row[3], "created_at": row[4], "tags": row[5]} 
        for row in cursor.fetchall()
    ]

@app.get("/stats", tags=["Administration"])
def get_stats(user: str = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM notes WHERE user = ?", (user,))
    count = cursor.fetchone()[0]
    return {"user": user, "total_notes": count, "system_status": "Secure"}

@app.delete("/notes/{note_id}", tags=["Notizen"])
def delete_note(note_id: int, user: str = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM notes WHERE id = ? AND user = ?", (note_id, user))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden oder keine Berechtigung")
    db.commit()
    return {"status": "success", "message": f"Notiz {note_id} gelöscht"}

@app.put("/notes/{note_id}", response_model=Note, tags=["Notizen"])
def update_note(note_id: int, note: NoteCreate, user: str = Depends(get_current_user), db=Depends(get_db)):
    """Aktualisiert eine vorhandene Notiz (Titel, Inhalt, Tags)."""
    cursor = db.cursor()
    cursor.execute(
        "UPDATE notes SET title = ?, content = ?, tags = ? WHERE id = ? AND user = ?",
        (note.title, note.content, note.tags, note_id, user)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden oder keine Berechtigung")
    db.commit()
    
    cursor.execute("SELECT id, title, content, user, created_at, tags FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    return {"id": row[0], "title": row[1], "content": row[2], "user": row[3], "created_at": row[4], "tags": row[5]}

app.mount("/static", StaticFiles(directory="static"), name="static")