---
marp: true
theme: gaia
class: invert
paginate: true
backgroundColor: #1e1e1e
color: #e0e0e0
---

#  Secure Notes Enterprise
## Praxisprojekt Lernfeld 11a
### DevSecOps: Sichere REST-API & Moderne Architektur

**Vorgelegt von: Tim Gromeyer**
**Datum: 24. Februar 2026**

---

## 1. Das Projektziel
- **Mission:** Eine hochsichere Web-API zur Verwaltung sensibler Notizen.
- **Problem:** Unverschlüsselte Speicherung und fehlende Zugriffskontrolle in Altsystemen.
- **Lösung:** 
  - **FastAPI Backend** (Asynchron & Schnell)
  - **SQLite** mit Prepared Statements
  - **Docker** für konsistente Deployment-Umgebungen

---

## 2. Schutzbedarfsanalyse (BSI 200-2)
- **Vertraulichkeit:** **HOCH** (Private Notizen)
- **Integrität:** **HOCH** (Schutz vor Manipulation)
- **Verfügbarkeit:** **NORMAL**

> **Risikoanalyse:** Fokus auf Schutz gegen SQL-Injection, Brute-Force und Man-in-the-Middle (MITM).

---

## 3. IT-Sicherheits-Features (LF11a Fokus)
- **Salted Hashing:** Passwörter werden mit SHA-256 und individuellem Salt gespeichert.
- **Sicheres Session-Management:** DB-gestützte Session-Tokens und HTTPS/TLS 1.3 Zwang.
- **Audit Logging:** Lückenlose, revisionssichere Protokollierung aller Aktionen.
- **Offline-First:** Lokales Hosting aller Bibliotheken für maximalen Datenschutz.

---

## 4. Systemarchitektur (Modular & Sicher)
- **Separation of Concerns:**
  - `auth.py`: Identitätsmanagement & Hashing
  - `database.py`: Persistenzschicht & Audit-Log
  - `models.py`: Datenstrukturen
  - `main.py`: API-Routing & Logik
- **Sicherheits-Härtung:** Strikte Content-Security-Policy (CSP) und CORS-Regeln.

---

## 5. Moderne Infrastruktur: Docker
- **Containerisierung:** Vollständige Kapselung der Anwendung.
- **Docker Compose:** Orchestrierung von API und Volumen.
- **Vorteile:**
  - "Works on my machine" Garantie.
  - Sichere Isolation vom Host-System.
  - **Hot-Reload:** Effiziente Entwicklung im Container.

---

## 6. Live-Demo & Testing
- **Dashboard:** Modernes UI mit Echtzeit-Suche & Tagging.
- **Tests:** Automatisierte Unit-Tests für Sicherheitsfunktionen.
- **CI/CD:** GitHub Actions für automatische Qualitätssicherung.

---

## 7. Fazit & Ausblick
- **Erreicht:** Sicheres, modulares MVP nach BSI-Grundschutz.
- **Nächste Schritte:** 
  - Einführung von OAuth2/OIDC.
  - Argon2 für noch stärkeres Hashing.
  - Monitoring mit Prometheus/Grafana.

---

### Vielen Dank für Ihre Aufmerksamkeit!
#### Fragen?
*(Dashboard erreichbar unter https://localhost:8000)*