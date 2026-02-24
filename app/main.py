import secrets
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

# Lokale Importe
from .database import get_db, log_action
from .models import NoteCreate, Note, LoginRequest
from .auth import get_current_user, verify_password, hash_password, session_scheme

app = FastAPI(
    title="Secure Notes Enterprise API",
    description="Vollstaendig revisionssichere Notiz-Verwaltung (Audit-Logs, Hashing, Docker, Export).",
    version="2.5.0",
    docs_url=None,  # Deaktiviere Standard-Docs fuer lokale Offline-Nutzung
    redoc_url=None
)

# --- SECURITY HARDENING (BSI & OWASP Standards) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Session-Token", "Content-Type"],
)

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    # Vollstaendig lokal: CDNs entfernt fuer maximale Performance und Datenschutz (BSI)
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://fastapi.tiangolo.com;"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/vendor/swagger-ui-bundle.js",
        swagger_css_url="/static/vendor/swagger-ui.css",
    )

@app.get("/", include_in_schema=False)
async def read_root():
    return FileResponse('static/login.html')

@app.get("/login.html", include_in_schema=False)
async def read_login():
    return FileResponse('static/login.html')

@app.get("/dashboard.html", include_in_schema=False)
async def read_dashboard():
    return FileResponse('static/dashboard.html')

@app.get("/admin.html", include_in_schema=False)
async def read_admin():
    return FileResponse('static/admin.html')

@app.post("/register", tags=["Auth"])
def register(auth: LoginRequest, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (auth.username,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Benutzername bereits vergeben")
    hashed, salt = hash_password(auth.password)
    cursor.execute("INSERT INTO users (username, hashed_password, salt) VALUES (?, ?, ?)", 
                   (auth.username, hashed, salt))
    db.commit()
    log_action(db, auth.username, "Benutzer registriert")
    return {"message": "Registrierung erfolgreich"}

@app.post("/login", tags=["Auth"])
def login(auth: LoginRequest, db=Depends(get_db)):
    if not verify_password(auth.password, auth.username, db):
        log_action(db, auth.username, "Login-Fehler: Ungueltige Anmeldedaten")
        raise HTTPException(status_code=401, detail="Falsche Anmeldedaten")
    token = secrets.token_urlsafe(32)
    cursor = db.cursor()
    cursor.execute("INSERT INTO sessions (token, user) VALUES (?, ?)", (token, auth.username))
    db.commit()
    print(f"\n[DEBUG] Neuer Login fuer {auth.username}\n[DEBUG] Session-Token: {token}\n")
    log_action(db, auth.username, "Login erfolgreich")
    return {"token": token, "user": auth.username}

@app.post("/logout", tags=["Auth"])
def logout(token: str = Depends(session_scheme), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
    db.commit()
    log_action(db, "System", "Session beendet", details=f"Token gelöscht")
    return {"message": "Abgemeldet"}

@app.post("/notes", response_model=Note, tags=["Notizen"])
def create_note(note: NoteCreate, user: str = Depends(get_current_user), db=Depends(get_db)):
    created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    cursor = db.cursor()
    cursor.execute("INSERT INTO notes (title, content, user, created_at, tags) VALUES (?, ?, ?, ?, ?)", 
                   (note.title, note.content, user, created_at, note.tags))
    db.commit()
    note_id = cursor.lastrowid
    log_action(db, user, "Notiz erstellt", note_id)
    return {"id": note_id, "title": note.title, "content": note.content, "user": user, "created_at": created_at, "tags": note.tags}

@app.get("/notes", response_model=List[Note], tags=["Notizen"])
def get_notes(q: Optional[str] = None, user: str = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor()
    if q:
        query = "SELECT id, title, content, user, created_at, tags FROM notes WHERE user = ? AND (title LIKE ? OR content LIKE ? OR tags LIKE ?) ORDER BY id DESC"
        cursor.execute(query, (user, f"%{q}%", f"%{q}%", f"%{q}%"))
    else:
        cursor.execute("SELECT id, title, content, user, created_at, tags FROM notes WHERE user = ? ORDER BY id DESC", (user,))
    return [{"id": row[0], "title": row[1], "content": row[2], "user": row[3], "created_at": row[4], "tags": row[5]} for row in cursor.fetchall()]

@app.get("/export", tags=["Notizen"])
def export_notes(user: str = Depends(get_current_user), db=Depends(get_db)):
    """Exportiert alle Notizen des Benutzers als JSON-Datei (DSGVO Datenportabilitaet)."""
    cursor = db.cursor()
    cursor.execute("SELECT title, content, created_at, tags FROM notes WHERE user = ?", (user,))
    notes = [{"title": row[0], "content": row[1], "created_at": row[2], "tags": row[3]} for row in cursor.fetchall()]
    log_action(db, user, "Datenexport durchgefuehrt")
    return JSONResponse(
        content=notes,
        headers={"Content-Disposition": f"attachment; filename=notes_export_{user}.json"}
    )

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
        log_action(db, user, "Loeschversuch fehlgeschlagen", note_id)
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    db.commit()
    log_action(db, user, "Notiz geloescht", note_id)
    return {"status": "success"}

@app.put("/notes/{note_id}", response_model=Note, tags=["Notizen"])
def update_note(note_id: int, note: NoteCreate, user: str = Depends(get_current_user), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE notes SET title = ?, content = ?, tags = ? WHERE id = ? AND user = ?", (note.title, note.content, note.tags, note_id, user))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    db.commit()
    log_action(db, user, "Notiz aktualisiert", note_id)
    cursor.execute("SELECT id, title, content, user, created_at, tags FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    return {"id": row[0], "title": row[1], "content": row[2], "user": row[3], "created_at": row[4], "tags": row[5]}

@app.get("/admin/logs", tags=["Administration"])
def get_audit_logs(user: str = Depends(get_current_user), db=Depends(get_db)):
    if user != "admin":
        raise HTTPException(status_code=403, detail="Keine Administratorrechte")
    cursor = db.cursor()
    cursor.execute("SELECT id, timestamp, user, action, resource_id, details FROM audit_logs ORDER BY id DESC LIMIT 100")
    return [{"id": row[0], "timestamp": row[1], "user": row[2], "action": row[3], "resource_id": row[4], "details": row[5]} for row in cursor.fetchall()]

@app.get("/admin/users", tags=["Administration"])
def get_all_users(user: str = Depends(get_current_user), db=Depends(get_db)):
    if user != "admin":
        raise HTTPException(status_code=403, detail="Keine Administratorrechte")
    cursor = db.cursor()
    cursor.execute("SELECT username FROM users")
    return [{"username": row[0]} for row in cursor.fetchall()]

app.mount("/static", StaticFiles(directory="static"), name="static")