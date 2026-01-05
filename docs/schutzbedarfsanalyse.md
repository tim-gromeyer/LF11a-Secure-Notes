# Schutzbedarfsanalyse "Secure Notes API"

Gemäß BSI-Standard 200-2 wurde eine Schutzbedarfsanalyse für die Secure Notes API durchgeführt. Das System speichert und verarbeitet potenziell sensible Notizen von Benutzern.

## 1. Schutzziele

- **Vertraulichkeit**: Hoch (Sensible Daten dürfen nicht in fremde Hände gelangen).
- **Integrität**: Hoch (Notizen dürfen nicht unbemerkt manipuliert werden).
- **Verfügbarkeit**: Normal (Kurze Ausfälle der API sind tolerierbar, aber kein Datenverlust).

## 2. Feststellung des Schutzbedarfs

### Anwendung (Secure Notes API)
Die API-Komponenten verarbeiten sensible Informationen, daher vererbt sich der Schutzbedarf der Daten (Hoch) auf die Anwendung. Ein Ausfall (Verfügbarkeit) ist nur "Normal", aber die Integrität und Vertraulichkeit erfordern einen **hohen** Schutzbedarf.

### IT-System (Server/Backend)
Der Server, auf dem das Backend und die SQLite-Datenbank laufen, muss stark abgesichert werden. Entsprechend wird der Schutzbedarf als **Hoch** eingestuft. Maßnahmen wie OS-Härtung, Firewalls (iptables/nftables) und aktuelle TLS-Zertifikate (Let's Encrypt) sind zwingend erforderlich.

### Netz (Kommunikation)
Da die API über das Internet erreichbar sein soll, besteht ein **hoher** Schutzbedarf für die Kommunikationstransparenz und Vertraulichkeit. Nur verschlüsselte Verbindungen über TLS 1.3 sind erlaubt.