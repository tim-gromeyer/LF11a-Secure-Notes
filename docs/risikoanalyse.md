# Risikoanalyse: Secure Notes Enterprise

Diese Risikoanalyse bewertet die potenziellen Gefährdungen des Projekts basierend auf den Kernaspekten der LF11a-Anforderungen.

## 1. Bewertung der Projektaspekte

| Aspekt | Status | Risiko | Bewertung & Maßnahme |
| :--- | :---: | :---: | :--- |
| **Schutzbedarf** | Identifiziert | HOCH | Vertraulichkeit und Integrität der Notizen sind kritisch. Maßnahme: Salted Hashing & TLS. |
| **Absicherung** | Implementiert | NIEDRIG | Schutz gegen SQL-Injection, Brute-Force und Timing-Attacks ist aktiv. |
| **Tests** | Erweitert | NIEDRIG | Automatisierte Pytests decken Auth-Flow und CRUD-Operationen ab. |
| **Backend** | Modular | MITTEL | Komplexität durch Session-Management. Maßnahme: Audit-Logging zur Überwachung. |
| **Projektziel** | Erreicht | NIEDRIG | Ziel der sicheren, revisionssicheren Notiz-Verwaltung ist vollständig umgesetzt. |
| **Umsatzplan** | Geplant | MITTEL | Umsetzung der technischen Anforderungen in 40h. Zeitpuffer für Refactoring wurde genutzt. |

## 2. Bedrohungsmatrix

| Bedrohung | Ursache | Auswirkung | Gegenmaßnahme |
| :--- | :--- | :--- | :--- |
| **SQL-Injection** | Manipulation von API-Eingaben | Datenverlust, Exfiltration | **Parameterisierte Abfragen** (SQLite) |
| **Brute-Force** | Erraten von Passwörtern | Unbefugter Zugriff | **Salted SHA-256 Hashing**, Rate Limiting |
| **Man-in-the-Middle** | Abhören unverschlüsselter Kommunikation | Passwortdiebstahl | **HTTPS / TLS 1.3** (Zertifikate vorhanden) |
| **Privilegieneskalation** | Fehlerhafte Berechtigungsprüfung | Zugriff auf fremde Notizen | **Ownership-Check** auf Datenbankebene |
| **Datenverlust** | Technischer Defekt, Fehlbedienung | Verlust sensibler Notizen | **Export-Funktion**, Docker-Volume Backups |

## 3. Risikobehandlung (Beispiele)

### Risiko: Kompromittierung von Benutzer-Hashes
*   **Behandlung:** Reduzierung durch Einsatz von individuellen **Salts**. Selbst bei Diebstahl der Datenbank können Passwörter nicht mittels Rainbow-Tables entschlüsselt werden.

### Risiko: Sitzungsdiebstahl (Session Hijacking)
*   **Behandlung:** Reduzierung durch **kryptografisch sichere Tokens** (`secrets.token_urlsafe`) und zeitnahe Löschung der Session bei Logout. Schutz durch HTTPS-Zwang in Produktion.

### Risiko: Compliance-Verstoß (Fehlende Nachvollziehbarkeit)
*   **Behandlung:** Vollständige Vermeidung durch Implementierung eines **revisionssicheren Audit-Loggings**, das jede Änderung protokolliert.
