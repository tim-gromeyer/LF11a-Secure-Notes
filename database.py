import sqlite3

def get_db():
    conn = sqlite3.connect("notes.db", check_same_thread=False)
    # Tabellen erstellen
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
    return conn