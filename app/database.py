import sqlite3

def get_db():
    conn = sqlite3.connect("notes.db", check_same_thread=False)
    # Revisionssichere Tabellen fuer Notizen und Sessions
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY, 
            title TEXT,
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
    # NEU: Benutzer-Tabelle fuer persistente Speicherung (DSGVO konform gehasht)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            hashed_password TEXT,
            salt TEXT
        )
    """)
    # NEU: Audit-Logs fuer Revisionssicherheit (BSI APP.3.1)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            user TEXT,
            action TEXT,
            resource_id INTEGER,
            details TEXT
        )
    """)
    return conn

def log_action(db, user, action, resource_id=None, details=""):
    """
    Hilfsfunktion zum Protokollieren von Sicherheits-relevanten Ereignissen.
    Wichtig fuer die Nachvollziehbarkeit gemaess BSI-Grundschutz.
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    db.execute(
        "INSERT INTO audit_logs (timestamp, user, action, resource_id, details) VALUES (?, ?, ?, ?, ?)",
        (timestamp, user, action, resource_id, details)
    )
    db.commit()