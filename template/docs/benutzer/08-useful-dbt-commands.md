[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 5. Useful dbt Commands

### 5.1 Basis-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `dbt debug` | Verbindung testen |
| `dbt deps` | Packages installieren/updaten |
| `dbt compile` | SQL generieren ohne Ausführung |
| `dbt run` | Alle Models bauen |
| `dbt test` | Tests ausführen |
| `dbt docs generate` | Dokumentation generieren |
| `dbt docs serve` | Dokumentation im Browser anzeigen |

### 5.2 Selektion

| Befehl | Beschreibung |
|--------|--------------|
| `dbt run --select model_name` | Einzelnes Model |
| `dbt run --select +model_name` | Model + Upstream |
| `dbt run --select model_name+` | Model + Downstream |
| `dbt run --select +model_name+` | Alles |
| `dbt run --select staging.*` | Alle Staging Models |
| `dbt run --select tag:hub` | Models mit Tag |

### 5.3 Full Refresh

```bash
# Inkrementelle Models neu bauen (DROP + CREATE)
dbt run --full-refresh
dbt run --full-refresh --select hub_company_client
```

---

◀ [Neue Entity hinzufügen](07-neue-entity-hinzufuegen.md) · [Übersicht](README.md) · [Troubleshooting](09-troubleshooting.md) ▶
