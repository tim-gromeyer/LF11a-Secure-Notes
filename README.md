# Praxisprojekt LF11a: Secure Notes Enterprise

Ein hochsicheres Fullstack-Projekt zur Erfüllung der Lernfeld 11a Anforderungen, mit Fokus auf IT-Sicherheit, BSI-konforme Schutzbedarfsanalyse und moderne DevSecOps-Workflows.

## Key Features
- **Sichere Authentifizierung:** Salted SHA-256 Hashing und DB-gestütztes Session-Token-Management.
- **Revisionssicherheit:** Lückenloses Audit-Logging aller sicherheitsrelevanten Aktionen.
- **Offline-First:** Vollständig lokale Bereitstellung von Bibliotheken (Swagger UI, Marked.js) für maximalen Datenschutz.
- **Interaktives Frontend:** Modernes Dashboard mit Live-Markdown-Vorschau und Echtzeit-Synchronisation.
- **Datenportabilität:** Integrierte Export-Funktion (JSON) gemäß DSGVO-Standards.
- **Infrastruktur:** Containerisierung via Docker (Alpine Linux) und lokales HTTPS/TLS Setup.

## Projektstruktur
- `app/`: Modulare Backend-Logik (FastAPI, Auth, Database).
- `static/`: Modernes Frontend und lokal gehostete Vendor-Assets.
- `docs/`: Umfassende Dokumentation (BSI, Risikoanalyse, Tagebuch).
- `tests/`: Automatisierte Sicherheits- und Funktionstests (Pytest).

## Starten

1. **Mit Docker (empfohlen):**
   ```bash
   docker-compose up --build
   ```
   Die API ist unter `https://localhost:8000` erreichbar.

2. **Manuell (Lokal):**
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --reload --ssl-keyfile key.pem --ssl-certfile cert.pem
   ```
3. **API-Dokumentation:** `https://localhost:8000/docs`.

## Dokumentation
Alle Planungs- und Security-Dokumente befinden sich im Verzeichnis [`docs/`](./docs/):
- [Schutzbedarfsanalyse](./docs/schutzbedarfsanalyse.md)
- [Sicherheitskonzept](./docs/sicherheitskonzept.md)
- [Risikoanalyse](./docs/risikoanalyse.md)
- [Methodik & KI-Nutzung](./docs/methodik.md)
- [Projekttagebuch](./docs/projekttagebuch.md)
- [Präsentation (Marp/Markdown)](./docs/praesentation.md)
