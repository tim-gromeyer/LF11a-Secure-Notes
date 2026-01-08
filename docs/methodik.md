# Methodik und Werkzeugeinsatz

## Verwendete Werkzeuge
*   **Backend:** Python 3.11, FastAPI
*   **Frontend:** HTML5, CSS3 (Vanilla), JavaScript
*   **Infrastruktur:** Docker (Alpine Linux), Docker Compose
*   **KI-Unterstützung:** Gemini 2.0 Flash (via Gemini CLI)

## Dokumentation der KI-Nutzung
Zur Beschleunigung der Entwicklungsphase und für das architektonische Refactoring wurde das Sprachmodell **Gemini 2.0 Flash** eingesetzt. Die Interaktion erfolgte über die **Gemini CLI**, um eine direkte Integration in die Entwicklungsumgebung zu ermöglichen.

### Beispiel-Prompt (Initial-Setup)
> "Ich entwickle ein Abschlussprojekt für LF11a (IT-Sicherheit). Erstelle ein modulares FastAPI-Backend für eine 'Secure Notes Enterprise' Anwendung. Anforderungen: SQLite-Datenbank, Salted SHA-256 Hashing für Passwörter, Datenbank-basiertes Session-Management (kein JWT, sondern Tokens in DB) und vollständiger Schutz gegen SQL-Injection. Das System soll revisionssichere Audit-Logs für alle Aktionen führen. Trenne den Code sauber in app/main.py, app/auth.py und app/database.py auf."

## Eigenleistung (Manuelle Anteile)
Während die Kernlogik und die Sicherheitsarchitektur KI-gestützt entworfen wurden, wurden folgende Komponenten **vollständig manuell** entwickelt bzw. angepasst:

1.  **UI/UX-Design:** Das gesamte CSS-Layout, die Farbschemata und das responsive Design des Dashboards wurden händisch entworfen, um eine professionelle Business-Optik zu erzielen.
2.  **SVG-Ikonografie:** Die Integration und Auswahl der Vektor-Icons (SVG) erfolgte manuell, um auf unprofessionelle Emojis zu verzichten.
3.  **Frontend-Logik:** Die komplexe Synchronisation der interaktiven Markdown-Checkboxen (Regex-basierte Manipulation des Quelltexts im Browser) wurde eigenständig implementiert.
4.  **BSI-Mapping:** Die Zuordnung der technischen Features zu den spezifischen BSI-Grundschutz-Bausteinen wurde händisch auf Basis der aktuellen BSI-Kataloge vorgenommen.
5.  **Qualitätssicherung:** Manuelles Penetration-Testing der Endpunkte und Validierung der Sicherheits-Header (CSP/CORS).
