# Projekttagebuch: Secure Notes Enterprise
**Name:** Tim Gromeyer
**Projektzeitraum:** 05.01.2026 – 09.01.2026 (Praxisphase)

## Woche 1: Planung & Kernentwicklung

### Montag, 05.01.2026
*   **Vormittag:** Durchführung der Schutzbedarfsanalyse nach BSI-Standard 200-2. Definition der Schutzziele (Vertraulichkeit, Integrität).
*   **Mittag:** Erstellung der ersten UML-Diagramme (Use-Case & Klassendiagramm). Setup der Projektstruktur.
*   **Nachmittag:** Implementierung des Basis-Backends mit FastAPI und SQLite. Erstellung der ersten Endpunkte für Notizen (CRUD).

### Dienstag, 06.01.2026
*   **Vormittag:** Fokus IT-Sicherheit: Umstellung der Passwort-Speicherung auf Salted Hashing (SHA-256).
*   **Nachmittag:** Erweiterung der API um Enterprise-Features: Einführung von Tags/Kategorien und einer serverseitigen Suchfunktion. Anpassung der Datumsformate auf deutsche Lokalisierung.

### Mittwoch, 07.01.2026
*   **Vormittag:** Refactoring der Authentifizierung: Ablösung von Basic Auth durch ein sichereres, Datenbank-gestütztes Session-Token-System.
*   **Nachmittag:** Große Code-Modularisierung: Trennung der Logik in `app/`, `auth/` und `database/` zur Verbesserung der Wartbarkeit (Clean Architecture).

### Donnerstag, 08.01.2026
*   **Vormittag:** Containerisierung der Anwendung. Erstellung des Dockerfiles auf Basis von Alpine Linux zur Minimierung der Angriffsfläche.
*   **Nachmittag:** Frontend-Upgrade: Implementierung eines Markdown-Renderers für formatierte Notizen. Integration von SVG-Icons zur Verbesserung der Professionalität.

### Freitag, 09.01.2026
*   **Vormittag:** Implementierung des Audit-Loggings und der Benutzer-Registrierung. Jede sicherheitsrelevante Aktion wird nun revisionssicher protokolliert.
*   **Mittag:** Entwicklung des Admin-Dashboards zur Einsicht der Audit-Logs. Implementierung der Live-Markdown-Vorschau und Daten-Export-Funktion.
*   **Nachmittag:** Sicherheits-Härtung: Umstellung auf lokales HTTPS, Verschärfung der Content-Security-Policy (CSP) und Migration auf eine Offline-First-Architektur durch lokales Hosting aller Vendor-Assets. Finales Testing.

---
**Gesamtaufwand:** ca. 38 Stunden