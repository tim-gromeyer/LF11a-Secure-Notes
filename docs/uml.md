# UML Diagramme (Aktualisiert)

## Use Case Diagramm
Dieses Diagramm zeigt die Interaktionen der Benutzer (User/Admin) mit dem System.

```mermaid
graph LR
    U((Benutzer))
    A((Administrator))

    U --> UC1(Registrieren)
    U --> UC2(Anmelden)
    U --> UC3(Notizen verwalten)
    U --> UC4(Daten exportieren)

    A --- U
    A --> UC5(Audit Logs einsehen)
    A --> UC6(Benutzerliste anzeigen)
```

## Sequenzdiagramm: Authentifizierung & Session (Login)
Detaillierter Ablauf des sicheren Logins mit Salted Hashing.

```mermaid
sequenceDiagram
    participant C as Client (Frontend)
    participant A as Auth-Modul (Backend)
    participant D as Database (SQLite)

    C->>A: POST /login (username, password)
    A->>D: SELECT hashed_password, salt FROM users WHERE ...
    D-->>A: Salt & Hash zurückgeben
    Note over A: input_hash = SHA256(password + salt)
    A->>A: secrets.compare_digest(input_hash, stored_hash)
    
    alt Erfolgreich
        Note over A: Generiere Session-Token (Secure Random)
        A->>D: INSERT INTO sessions (token, user)
        A-->>C: 200 OK (Token)
    else Fehlgeschlagen
        A-->>C: 401 Unauthorized
    end
```

## Sequenzdiagramm: Authentifizierte Anfrage (z.B. Notiz erstellen)
Zeigt die Validierung des Session-Tokens bei jeder Anfrage.

```mermaid
sequenceDiagram
    participant C as Client (Frontend)
    participant A as API / Auth Middleware
    participant D as Database (SQLite)

    C->>A: POST /notes (Header: X-Session-Token)
    A->>D: SELECT user FROM sessions WHERE token = ?
    
    alt Token gültig
        D-->>A: username
        A->>D: INSERT INTO notes (title, content, user, ...)
        A->>D: INSERT INTO audit_logs (action, user, ...)
        A-->>C: 200 OK (Erstellte Notiz)
    else Token ungültig
        D-->>A: NULL
        A-->>C: 401 Unauthorized
    end
```

## Klassendiagramm (Modular)
Struktur der Anwendung nach dem Refactoring.

```mermaid
classDiagram
    class Note {
        +int id
        +String title
        +String content
        +String tags
        +String created_at
    }
    
    class User {
        +String username
        +String hashed_password
        +String salt
    }

    class Auth {
        +hash_password(pass)
        +verify_password(pass, user)
        +get_current_user(token)
    }

    class Database {
        +get_db()
        +log_action(user, action)
    }

    Auth ..> User : validiert
    Auth ..> Database : nutzt
    Database -- Note : speichert
```