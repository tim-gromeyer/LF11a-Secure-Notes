# Schutzbedarfsanalyse & Risikoanalyse (LF11a)

## 1. Schutzbedarfsanalyse (BSI 200-2)

Das System "Secure Notes Enterprise" wurde nach den Kriterien des BSI-Grundschutzes bewertet.

| Objekt | Vertraulichkeit | Integrität | Verfügbarkeit |
| :--- | :---: | :---: | :---: |
| **Benutzer-Notizen** | HOCH | HOCH | NORMAL |
| **Authentifizierungs-Daten** | SEHR HOCH | HOCH | HOCH |
| **API-Infrastruktur** | NORMAL | HOCH | NORMAL |

**Begründung:**
- **Vertraulichkeit:** Da Notizen private oder geschäftliche Geheimnisse enthalten können, ist der Schutz vor unbefugter Einsicht kritisch (HOCH).
- **Integrität:** Eine unbemerkte Änderung von Notizen könnte fatale Folgen haben (z. B. falsche Passwörter oder Anweisungen) (HOCH).
- **Verfügbarkeit:** Ein kurzzeitiger Ausfall ist für den Nutzer ärgerlich, aber nicht geschäftskritisch (NORMAL).

## 2. Risikoanalyse

| Bedrohung | Eintrittswahrscheinlichkeit | Auswirkung | Risiko-Stufe | Gegenmaßnahme |
| :--- | :---: | :---: | :---: | :--- |
| **SQL-Injection** | Mittel | Hoch | **Hoch** | Prepared Statements (aktiv) |
| **Brute-Force Login** | Hoch | Mittel | **Mittel** | Rate Limiting & Starke Passwörter |
| **Man-in-the-Middle** | Mittel | Hoch | **Hoch** | TLS 1.3 Verschlüsselung |
| **Unbefugter Zugriff** | Niedrig | Hoch | **Mittel** | Horizontale Autorisierung (aktiv) |

## 3. Technisch-organisatorische Maßnahmen (TOMs)

Gemäß Art. 32 DSGVO wurden folgende Maßnahmen getroffen:

### Pseudonymisierung & Verschlüsselung
- **Transportverschlüsselung:** Einsatz von TLS für alle API-Aufrufe.
- **Passwort-Schutz:** Passwörter werden im Backend niemals im Klartext verarbeitet (Salted Hashing).

### Vertraulichkeit (Zutritt, Zugang, Zugriff)
- **Zugangskontrolle:** Authentifizierung via DB-gestütztem Session-Management (Tokens).
- **Zugriffskontrolle:** Rollenbasierte Autorisierung (RBAC) auf Datenbankebene durch `user`-ID Filterung.

### Integrität (Weitergabe, Eingabe)
- **Eingabekontrolle:** Validierung aller API-Anfragen durch Pydantic-Modelle.
- **Datenträgerkontrolle:** Sicherung der SQLite-Datenbank durch Dateisystemrechte.

### Verfügbarkeit & Belastbarkeit
- **Backups:** Regelmäßige Exporte der SQLite-Datenbank.
- **Wiederherstellbarkeit:** Automatisierte Deployment-Skripte für schnellen Wiederanlauf (CI/CD).