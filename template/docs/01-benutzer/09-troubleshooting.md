---
title: "Troubleshooting"
tags:
  - benutzer
  - typ/troubleshooting
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 6. Troubleshooting

### 6.1 Verbindungsprobleme

**Symptom:** `Login failed`
```bash
# Bei Azure-CLI-Authentifizierung: Token erneuern
az login
az account set --subscription "<subscription-id>"
dbt debug
```
Bei SQL-Authentifizierung: Benutzer und Passwort im Profil prüfen (abgelaufene Passwörter melden).

**Symptom:** `Connection timeout`
```bash
# Firewall prüfen
az sql server firewall-rule list \
  --resource-group <resource-group> \
  --server <sql-server>
```

### 6.2 External Table Fehler

**Symptom:** `External table error`
```bash
# External Tables neu erstellen
dbt run-operation stage_external_sources

# Prüfen ob Parquet-Dateien existieren
# (Im Azure Portal: Storage Account → Container der Landing Zone)
```

### 6.3 Model-Fehler

**Symptom:** Kompilierungsfehler
```bash
# SQL anzeigen
dbt compile --select problem_model

# Generiertes SQL prüfen
cat target/compiled/datavault/models/path/to/model.sql
```

**Symptom:** `Columnstore not supported`
```yaml
# In dbt_project.yml oder Model-Config
+as_columnstore: false
```

### 6.4 Logs prüfen

```bash
# dbt Logs
less logs/dbt.log

# Letzte Queries
cat logs/query_log.sql

# Run Results
cat target/run_results.json | jq '.results[] | {model: .unique_id, status: .status}'
```

---

◀ [Useful dbt Commands](08-useful-dbt-commands.md) · [Übersicht](README.md) · [Daten prüfen](10-daten-pruefen.md) ▶
