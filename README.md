# Praxisprojekt LF11b: Secure Notes API

Ein praxisorientiertes Backend-Projekt zur Erfüllung der Lernfeld 11b (LF11b) Anforderungen, mit starkem Fokus auf IT-Sicherheit, Schutzbedarfsanalyse und BSI-Grundschutz.

## Features
- REST-API mit Python (FastAPI)
- Integrierte API-Dokumentation (OpenAPI/Swagger unter `/docs`)
- Authentifizierung über HTTP Basic Auth
- SQLite-Datenbank (sicher gegen SQL-Injections)
- Unit-Tests & CI-Pipeline (GitHub Actions)
- Umfassende Markdown-Dokumentation (Schutzbedarf, BSI-Bausteine, UML)

## Starten

1. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
2. Server starten:
   ```bash
   uvicorn main:app --reload
   ```
3. API aufrufen unter `http://127.0.0.1:8000/docs`. (User: `admin`, Pass: `secret`)

## Tests ausführen
```bash
pytest test_main.py
```

## Dokumentation
Alle relevanten Planungs- und Security-Dokumente befinden sich im Verzeichnis [`docs/`](./docs/). Die Präsentation liegt als [`praesentation.md`](./praesentation.md) bei (kann z.B. mit Marp gerendert werden oder einfach als Markdown betrachtet werden).