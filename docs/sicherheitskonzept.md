# Sicherheitskonzept: Secure Notes API (LF11a)

Dieses Dokument beschreibt die detaillierten Sicherheitsmechanismen, die in der Secure Notes API implementiert wurden, um die Schutzziele Vertraulichkeit, Integrität und Verfügbarkeit zu gewährleisten.

## 1. Identitäts- und Zugriffsbeschränkung (IAM)

### Authentifizierung
Die Anwendung nutzt **HTTP Basic Authentication**. Der Zugriff auf sensible Endpunkte (`/notes`) ist nur mit gültigen Anmeldedaten möglich.
- **Sicherheitsmerkmal:** Verwendung von `secrets.compare_digest`. Dies verhindert **Timing-Attacks**, bei denen Angreifer durch Messung der Antwortzeit Rückschlüsse auf die Korrektheit einzelner Zeichen des Passworts ziehen könnten.

### Autorisierung (Ownership-Prinzip)
Es wird eine strikte Trennung der Benutzerdaten erzwungen.
- **Mechanismus:** Bei jedem Datenbankzugriff (READ, DELETE) wird zwingend die Benutzer-ID in der `WHERE`-Klausel geprüft (`WHERE id = ? AND user = ?`).
- **Schutz vor:** Horizontaler Privilegieneskalation (ein Benutzer greift auf Daten eines anderen Benutzers zu).

## 2. Schutz vor Injection-Angriffen

### SQL-Injection
Die Anwendung ist immun gegen klassische SQL-Injection-Angriffe.
- **Maßnahme:** Einsatz von **Prepared Statements** (parametrisierte Abfragen) über das `sqlite3`-Modul. Benutzereingaben werden niemals direkt in den SQL-String verkettet, sondern als Parameter (`?`) übergeben.

### Input-Validierung (Schema-Enforcement)
Durch den Einsatz von **Pydantic** in FastAPI werden alle eingehenden JSON-Payloads gegen vordefinierte Schemata validiert.
- **Sicherheitsgewinn:** Ungültige Datentypen oder übermäßig große Payloads werden bereits auf Framework-Ebene abgelehnt, bevor sie die Geschäftslogik erreichen.

## 3. Kryptografie und Datentransfer

### TLS (Transport Layer Security)
Obwohl im lokalen Entwicklungsmodus HTTP verwendet wird, ist das System für den Betrieb hinter einem Reverse-Proxy (z. B. Nginx oder Traefik) mit **TLS 1.3** konzipiert.
- **HSTS (HTTP Strict Transport Security):** In der Produktionskonfiguration wird HSTS empfohlen, um Downgrade-Angriffe zu verhindern.

### Passwort-Hashing (Ausblick)
Im aktuellen Prototyp werden Passwörter im Speicher verglichen. Für die produktive Version ist die Integration von **Argon2** oder **bcrypt** zur sicheren Speicherung von Passwort-Hashes in der Datenbank vorgesehen.

## 4. Sicherheit im Entwicklungsprozess (DevSecOps)

### Automatisierte Tests
Jeder Sicherheits-Endpunkt wird durch Unit-Tests in `test_main.py` geprüft.
- **Testszenarien:** Erfolgreiche Anmeldung, Abgebrochene Anmeldung (401 Unauthorized), Zugriff auf nicht existierende Ressourcen.

### CI-Pipeline (GitHub Actions)
Durch die integrierte CI-Pipeline wird sichergestellt, dass keine Code-Änderungen übernommen werden, die die bestehenden Sicherheitstests verletzen.

## 5. Infrastruktur-Härtung (BSI-Konformität)

Basierend auf den BSI-Grundschutz-Bausteinen werden folgende Maßnahmen für das Hosting empfohlen:
- **Firewall:** Restriktive Regeln (nur Port 443 offen).
- **Least Privilege:** Der API-Prozess läuft unter einem dedizierten Service-User ohne Root-Rechte.
- **Logging:** Revisionssicheres Logging von fehlgeschlagenen Anmeldeversuchen zur Erkennung von Brute-Force-Angriffen.