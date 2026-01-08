import secrets
import hashlib
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from database import get_db

session_scheme = APIKeyHeader(name="X-Session-Token")

# Benutzer-Datenbank (Demo)
USER_DB = {
    "admin": {
        "salt": "lf11a_salt_demo",
        "hashed_password": hashlib.sha256(("secret" + "lf11a_salt_demo").encode()).hexdigest()
    }
}

def verify_password(plain_password, username):
    user_record = USER_DB.get(username)
    if not user_record:
        return False
    input_hash = hashlib.sha256((plain_password + user_record["salt"]).encode()).hexdigest()
    return secrets.compare_digest(input_hash, user_record["hashed_password"])

def get_current_user(token: str = Depends(session_scheme), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT user FROM sessions WHERE token = ?", (token,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session abgelaufen oder ungültig",
        )
    return row[0]