# BSI-Grundschutz-Bausteine "Secure Notes Enterprise"

Zur Erfüllung des festgestellten Schutzbedarfs wurden folgende BSI-Grundschutz-Bausteine als relevant identifiziert und in der Projekt-Architektur umgesetzt:

## APP.3.1 Webanwendungen
- **Eingabe-Validierung:** Strikte Typisierung und Schema-Enforcement durch Pydantic (FastAPI).
- **Injection-Schutz:** Konsequente Nutzung von Prepared Statements (SQLite) zur Verhinderung von SQL-Injection.
- **Sichere Authentifizierung:** Implementierung eines DB-gestützten Session-Token-Verfahrens zur Minimierung der Passwort-Exposition.
- **Sicherheits-Header:** Konfiguration von Content-Security-Policy (CSP) und HSTS zur Abwehr von XSS und Downgrade-Angriffen.

## CON.2 Kryptografie
- **Passwort-Schutz:** Einsatz von **Salted SHA-256 Hashing**. Passwörter werden niemals im Klartext gespeichert.
- **Transport-Verschlüsselung:** Erzwingung von TLS 1.3 für alle Verbindungen.
- **Zufallszahlen:** Nutzung von `secrets.token_urlsafe` für kryptografisch sichere Session-Identifikatoren.

## NET.3.2 Firewall
- **Restriktive Ports:** Ausschließlich Port 443 (HTTPS) ist für den Anwendungszugriff vorgesehen.
- **Infrastruktur-Isolation:** Betrieb der Anwendung in isolierten Docker-Containern zur Trennung vom Host-System.

## SYS.1.1 Allgemeine Server
- **Minimale Angriffsfläche:** Verwendung von **Alpine Linux** als Basis-Image für den Container zur Reduzierung potenzieller Schwachstellen.
- **Logging:** Implementierung eines revisionssicheren **Audit-Log-Systems** zur lückenlosen Nachvollziehbarkeit administrativer und benutzerbezogener Aktionen.
