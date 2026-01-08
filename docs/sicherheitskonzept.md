# Sicherheitskonzept: Secure Notes Enterprise (LF11a)

Dieses Dokument beschreibt die detaillierten Sicherheitsmechanismen, die in der Secure Notes API implementiert wurden, um die Schutzziele Vertraulichkeit, Integrität und Verfügbarkeit zu gewährleisten.

## 1. Identitäts- und Zugriffsbeschränkung (IAM)

### Authentifizierung & Passwort-Schutz
Die Anwendung nutzt ein **Session-Token-Verfahren** in Kombination mit einem modernen Hashing-Verfahren.
- **Salted SHA-256 Hashing:** Passwörter werden niemals im Klartext gespeichert oder verglichen. Stattdessen wird jedem Passwort ein eindeutiger "Salt" hinzugefügt, bevor es gehasht wird. Dies schützt vor **Rainbow-Table-Angriffen**.
- **Sicherheitsmerkmal:** Verwendung von `secrets.compare_digest` für den Hash-Vergleich. Dies verhindert **Timing-Attacks**.

### Autorisierung (Ownership-Prinzip)
Es wird eine strikte Trennung der Benutzerdaten erzwungen.
- **Mechanismus:** Bei jedem Datenbankzugriff (READ, UPDATE, DELETE) wird zwingend die Benutzer-ID in der `WHERE`-Klausel geprüft (`WHERE id = ? AND user = ?`).
- **Schutz vor:** Horizontaler Privilegieneskalation (ein Benutzer greift auf Daten eines anderen Benutzers zu).

## 2. Schutz vor Injection-Angriffen

### SQL-Injection
Die Anwendung ist immun gegen klassische SQL-Injection-Angriffe.
- **Maßnahme:** Einsatz von **Prepared Statements** (parametrisierte Abfragen) über das `sqlite3`-Modul. Benutzereingaben werden niemals direkt in den SQL-String verkettet, sondern als Parameter (`?`) übergeben.

### Input-Validierung (Schema-Enforcement)
Durch den Einsatz von **Pydantic** in FastAPI werden alle eingehenden JSON-Payloads gegen vordefinierte Schemata validiert.
- **Sicherheitsgewinn:** Ungültige Datentypen oder bösartige Payloads werden bereits auf Framework-Ebene abgelehnt, bevor sie die Geschäftslogik erreichen.

## 3. Kryptografie und Datentransfer

### TLS (Transport Layer Security)
Die gesamte Kommunikation erfolgt über **HTTPS / TLS 1.3**. 
- **Entwicklung:** Auch in der lokalen Entwicklungsumgebung werden selbstsignierte Zertifikate genutzt, um ein identisches Sicherheitsniveau wie in Produktion zu gewährleisten.
- **HSTS (HTTP Strict Transport Security):** Verhindert Downgrade-Angriffe auf unverschlüsseltes HTTP.

## 4. Infrastruktur-Sicherheit (Docker & Alpine)

Die Anwendung wird in einem Docker-Container bereitgestellt, wobei **Alpine Linux** als Basis-Image dient.
- **Reduzierte Angriffsfläche:** Alpine ist eine extrem schlanke Distribution, die nur die absolut notwendigen Pakete enthält. Dies minimiert die Anzahl potenzieller Schwachstellen (CVEs) im Betriebssystem des Containers.
- **Isolation:** Der Container isoliert die Anwendung vom Host-System.

## 5. Revisionssicherheit (Audit Logging)

Gemäß BSI-Anforderungen an Webanwendungen wurde ein **Audit-Log-System** implementiert.
- **Protokollierung:** Alle sicherheitsrelevanten Aktionen (Login, Registrierung, Änderungen an Notizen) werden mit Zeitstempel, Benutzer und Ressourcen-ID in einer separaten Datenbanktabelle gespeichert.
- **Admin-Dashboard:** Ein dedizierter Bereich erlaubt die Überwachung dieser Logs durch autorisierte Administratoren.

## 6. Verfügbarkeit & Datenschutz (Offline-First)

Um die Abhängigkeit von externen Ressourcen zu minimieren und den Datenschutz zu erhöhen, wurden alle Bibliotheken lokal eingebunden.
- **Lokal gehostete Ressourcen:** Swagger-UI (JS/CSS) und Marked.js befinden sich im Verzeichnis `static/vendor/`.
- **Sicherheitsvorteil:** Die Anwendung funktioniert vollständig ohne Internetverbindung und verhindert den Abfluss von Metadaten an Drittanbieter-CDNs.
- **CSP-Härtung:** Die Content-Security-Policy erlaubt keine externen Script-Quellen.

## 7. Sicherheit im Entwicklungsprozess (DevSecOps)

### Automatisierte Tests
Jeder Sicherheits-Endpunkt wird durch Unit-Tests in `tests/test_main.py` geprüft.
- **Test-Isolation:** Verwendung einer In-Memory SQLite-Datenbank für Tests, um die Integrität der lokalen Entwicklungsdatenbank nicht zu gefährden.

### CI-Pipeline (GitHub Actions)
Durch die integrierte CI-Pipeline wird sichergestellt, dass keine Code-Änderungen übernommen werden, die die bestehenden Sicherheitstests verletzen.
