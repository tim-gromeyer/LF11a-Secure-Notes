# BSI-Grundschutz-Bausteine "Secure Notes API"

Zur Erfüllung des festgestellten Schutzbedarfs wurden folgende BSI-Grundschutz-Bausteine als relevant identifiziert und in der Projektplanung berücksichtigt:

## APP.3.1 Webanwendungen
- Umsetzung von HTTP-Strict-Transport-Security (HSTS).
- Validierung aller Eingaben im Backend (wird durch Pydantic in FastAPI sichergestellt).
- Verhinderung von SQL-Injection durch Prepared Statements in SQLite.
- Umsetzung einer sicheren Authentifizierung (geplant: OAuth2, aktuell als Prototyp: HTTP Basic Auth über TLS).

## CON.2 Kryptografie
- Einsatz aktueller Verschlüsselungsverfahren.
- TLS 1.2 / TLS 1.3 für alle Verbindungen.
- Speicherung der Passwörter zukünftig mit starken Hashverfahren (z. B. Argon2). In der aktuellen Demo-Version zum Zwecke des Proof of Concepts rudimentär umgesetzt.

## NET.3.2 Firewall
- Absicherung des Backends hinter einer Firewall.
- Zugriff auf Port 22 (SSH) nur über VPN oder spezifische IP-Ranges.
- Ausschließlich Port 443 (HTTPS) ist öffentlich erreichbar.

## SYS.1.1 Allgemeine Server
- OS-Härtung des Host-Systems (z. B. Deaktivieren nicht benötigter Dienste, Root-Login per SSH deaktivieren).
- Regelmäßige, automatisierte Updates (Unattended Upgrades).