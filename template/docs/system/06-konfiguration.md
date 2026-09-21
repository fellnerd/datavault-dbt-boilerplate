[Dokumentation](../README.md) › [Data Vault 2.1 - Systemdokumentation](README.md)

# 6. Konfiguration

### 6.1 dbt_project.yml

Aufbau (gekürzt, massgeblich ist die Datei selbst):

```yaml
name: 'datavault'
profile: 'datavault'

on-run-end:
  - "{{ log_load_status() }}"        # Ladeprotokoll schreiben
  - "{{ grant_select_on_views() }}"  # OLS: SELECT-Grants auf mart*-Views setzen

dispatch:                            # eigene Macros vor automate_dv
  - macro_namespace: automate_dv
    search_order: ['datavault', 'automate_dv']

vars:
  hash: 'SHA'
  concat_string: '||'
  null_placeholder_string: '-1'
  hash_content_casing: 'DISABLED'
  escape_char_left: '['
  escape_char_right: ']'
  load_date: 'dss_load_date'
  record_source: 'dss_record_source'
  ols_view_grants: { <principal>: ['mart', 'mart_<domain>'] }

models:
  datavault:
    staging:
      +schema: stg
      +materialized: view
    raw_vault:
      _common:                       # Schema vault
        hubs:      { +schema: vault, +materialized: incremental,
                     +incremental_strategy: append, +on_schema_change: append_new_columns }
        satellites: { ... }
        links:      { ... }
        refs:       { +schema: vault, +materialized: view }
      <concept>:                     # Schema vault_<concept>, optional mit +tags
        hubs: { ... }
        satellites: { ... }
        links: { ... }
    business_vault:
      +schema: mart_<domain>
      +materialized: view
    mart:
      _common:   { +schema: mart,          +materialized: table, +as_columnstore: false }
      <domain>:  { +schema: mart_<domain>, +materialized: table, +as_columnstore: false }
```

Wichtige Punkte:

- **Schema-Konvention:** `stg` · `vault` / `vault_<concept>` · `mart` / `mart_<domain>`.
  Der dbt-Standard-Prefix wird von `generate_schema_name` unterdrückt.
- **Tags je Domäne:** Domänen mit eigenem Ladefenster (z. B. CDR-Massendaten, Energiedaten)
  tragen ein Tag und werden über eigene CI-Jobs geladen, nicht im regulären `dbt run`.
- **Business Vault liegt im Mart-Schema:** Objekte, die Power BI direkt konsumiert, dürfen
  nicht im `vault`-Schema liegen — Endnutzer sehen ausschliesslich `mart*`.
- **Seeds:** Standard-Schema `vault`; Seeds mit operativem Charakter (z. B. Berechtigungs-
  matrizen) werden explizit nach `stg` gelegt und erhalten `+column_types` (NVARCHAR für Umlaute).

### 6.2 Azure SQL — Einschränkungen und Konventionen

- ❌ Kein Columnstore Index in den genutzten Service-Tiers → `+as_columnstore: false` auf allen Tabellen
- ❌ Keine Cross-Database-Queries → immer `{{ target.database }}` bzw. `ref()`/`source()`
- ✅ External Tables auf ADLS Gen2 (PolyBase/OPENROWSET)
- ✅ Native Row-Level- und Column-Level-Security (siehe [Sicherheit](07-sicherheit.md))
- ⚠️ Inkrementelle Modelle laufen mit `incremental_strategy: append`; Schemaänderungen werden
  über `on_schema_change: append_new_columns` ergänzt, geänderte Hash-Inputs erfordern `--full-refresh`

---

◀ [Dateistruktur](05-dateistruktur.md) · [Übersicht](README.md) · [Sicherheit](07-sicherheit.md) ▶
