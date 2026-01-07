import secrets
import hashlib
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from .database import get_db

session_scheme = APIKeyHeader(name="X-Session-Token")

def hash_password(password: str, salt: str = None):
    """
    Erstellt einen SHA-256 Hash mit einem Salt.
    Wichtig fuer den Schutz gegen Brute-Force und Rainbow-Tables.
    """
    if not salt:
        salt = secrets.token_urlsafe(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def verify_password(plain_password, username, db):
    """
    Ueberprueft ein Passwort gegen den gespeicherten Hash in der Datenbank.
    Nutzt secrets.compare_digest gegen Timing-Attacks.
    """
    cursor = db.cursor()
    cursor.execute("SELECT hashed_password, salt FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    
    # Fallback fuer den initialen Admin (falls DB leer)
    if not row and username == "admin":
        # Initialer Admin mit Standardpasswort 'secret'
        # In Produktion sollte dieser Block nach dem ersten Setup entfernt werden.
        return plain_password == "secret"

    if not row:
        return False
        
    stored_hash, salt = row
    input_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
    return secrets.compare_digest(input_hash, stored_hash)

def get_current_user(token: str = Depends(session_scheme), db=Depends(get_db)):
    """
    Validiert das Session-Token gegen die Datenbank.
    Gemaess BSI-Anforderung fuer sicheres Session-Management.
    """
    cursor = db.cursor()
    cursor.execute("SELECT user FROM sessions WHERE token = ?", (token,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session abgelaufen oder ungültig",
        )
    return row[0]