from pydantic import BaseModel
from typing import Optional

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[str] = "Allgemein"

class Note(BaseModel):
    id: int
    title: str
    content: str
    user: str
    created_at: str
    tags: Optional[str]

class LoginRequest(BaseModel):
    username: str
    password: str