# UML Diagramme

## Use Case Diagramm
```mermaid
usecaseDiagram
    actor User
    usecase "Login / Authenticate" as UC1
    usecase "Create Note" as UC2
    usecase "Read Notes" as UC3

    User --> UC1
    User --> UC2
    User --> UC3
    UC2 ..> UC1 : include
    UC3 ..> UC1 : include
```

## Sequenzdiagramm: Notiz erstellen
```mermaid
sequenceDiagram
    participant C as Client (User)
    participant A as API (FastAPI)
    participant D as Database (SQLite)

    C->>A: POST /notes (Basic Auth, Content)
    A->>A: Validate Credentials
    alt Invalid Credentials
        A-->>C: 401 Unauthorized
    else Valid Credentials
        A->>D: INSERT INTO notes...
        D-->>A: Return new Row ID
        A-->>C: 200 OK (id, content)
    end
```

## Klassendiagramm
```mermaid
classDiagram
    class NoteCreate {
        +String content
    }
    class HTTPBasicCredentials {
        +String username
        +String password
    }
    class APIEndpoints {
        +create_note(NoteCreate, User, DB)
        +get_notes(User, DB)
    }
    class Database {
        +sqlite3.Connection
    }

    NoteCreate --> APIEndpoints : validiert
    HTTPBasicCredentials --> APIEndpoints : auth
    APIEndpoints --> Database : speichert
```