[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 7. Daten prüfen

### 7.1 Abfragen absetzen

Für Ad-hoc-Abfragen eignen sich SQL Server Management Studio, Azure Data Studio oder `sqlcmd`:

```bash
sqlcmd -S <sql-server>.database.windows.net -d <datenbank> -G \
  -Q "SELECT TOP 10 * FROM vault.hub_<entity>"
```

Innerhalb des Projekts geht es auch ohne Client:

```bash
dbt run-operation run_sql --args '{"sql": "SELECT COUNT(*) FROM vault.hub_<entity>"}'
```

### 7.2 Datenzählung

```sql
-- External Table (Rohdaten aus der Landing Zone)
SELECT COUNT(*) FROM stg.ext_<concept>_<entity>;

-- Staging View (mit Hashes und Metadaten)
SELECT COUNT(*) FROM stg.<concept>_<entity>;

-- Data Vault
SELECT COUNT(*) FROM vault.hub_<entity>;
SELECT COUNT(*) FROM vault.sat_<entity>__<quelle>;
```

Row Counts über alle Objekte auf einmal:

```bash
dbt run-operation log_row_counts
```

---

◀ [Troubleshooting](09-troubleshooting.md) · [Übersicht](README.md) · [Best Practices](11-best-practices.md) ▶
