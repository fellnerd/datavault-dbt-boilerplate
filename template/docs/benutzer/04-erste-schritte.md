[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 1. Erste Schritte

### 1.1 Voraussetzungen

- Arbeitsplatz oder Server mit Netzwerkzugang zur Azure-SQL-Datenbank (Firewall-Freigabe)
- Python 3.10+ mit virtueller Umgebung
- ODBC Driver 18 for SQL Server
- Zugangsdaten für das dbt-Profil (SQL-Login oder Azure CLI, je nach Umgebung)
- Lesezugriff auf das Git-Repository

### 1.2 Projekt Setup

```bash
# Projektverzeichnis
cd <pfad>/datavault-dbt

# Virtual Environment aktivieren
source .venv/bin/activate

# Packages installieren/aktualisieren
dbt deps
```

Die Verbindung wird über `~/.dbt/profiles.yml` (Profil `datavault`) konfiguriert; die Datei
liegt bewusst ausserhalb des Repositories. Bei Azure-CLI-Authentifizierung vorher `az login`
ausführen und mit `az account show` die Anmeldung prüfen.

### 1.3 dbt Verbindung testen

```bash
dbt debug --target <mandant>-dev
```

Erwartete Ausgabe:
```
  Connection:
    server: <sql-server>.database.windows.net
    database: <datenbank>
    schema: dv
  All checks passed!
```

---

◀ [Wichtige Spalten verstehen](03-wichtige-spalten-verstehen.md) · [Übersicht](README.md) · [Tägliche Operationen](05-taegliche-operationen.md) ▶
