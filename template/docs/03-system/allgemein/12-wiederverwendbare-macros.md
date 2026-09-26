---
title: "Wiederverwendbare Macros"
tags:
  - system
---
[Dokumentation](../../README.md) › [Data Vault 2.1 - Systemdokumentation](../README.md)

# 12. Wiederverwendbare Macros

### Vault- und Modellierung

| Macro | Datei | Beschreibung |
|-------|-------|--------------|
| `generate_schema_name` | `macros/generate_schema_name.sql` | Schema ohne dbt-Prefix |
| `sqlserver__cast_binary`, `sqlserver__type_string` | `macros/hash_override.sql` | automate_dv-Overrides: `CHAR(64)`-Hashes, NVARCHAR-Inputs |
| `update_satellite_current_flag` | `macros/satellite_current_flag.sql` | Post-Hook für `dss_is_current` |
| `update_effectivity_end_dates` | `macros/satellite_current_flag.sql` | End-Dating für Effectivity Satellites |
| `satellite_current_view` | `macros/satellite_current_view.sql` | Generiert `sat_*_current_v` |
| `zero_key` / `error_key` / `insert_ghost_records` | `macros/ghost_records.sql` | Ghost Records (64×`0` bzw. 64×`F`) |
| `surrogate_key` | `macros/surrogate_key.sql` | Deterministischer BIGINT-Surrogate-Key für Marts |

### Betrieb und Performance

| Macro | Datei | Beschreibung |
|-------|-------|--------------|
| `create_hash_index`, `create_composite_index`, `drop_and_create_index` | `macros/create_hash_index.sql` | Indizes auf Hash Keys / Spaltenkombinationen |
| `create_load_status_table`, `log_load_status` | `macros/create_load_status_table.sql` | Ladeprotokoll, als `on-run-end`-Hook aktiv |
| `log_row_counts` | `macros/log_row_counts.sql` | Row Counts je Objekt protokollieren |
| `cleanup_old_objects` | `macros/cleanup_old_objects.sql` | Abgelöste Datenbankobjekte entfernen |
| `measure_rls_overhead` | `macros/measure_rls_overhead.sql` | Laufzeit/Reads mit und ohne RLS vergleichen |
| `run_sql` | `macros/run_sql.sql` | Ad-hoc-SQL für Exploration |

### Quellen und External Tables

| Macro | Datei | Beschreibung |
|-------|-------|--------------|
| `create_external_table` | `macros/stage_external_sources_selective.sql` | Erstellt eine einzelne External Table aus `sources.yml` |
| `list_parquet_files` | `macros/list_parquet_files.sql` | Dateien eines Landing-Zone-Ordners auflisten |
| `get_parquet_schema` | `macros/get_parquet_schema.sql` | Schema einer Parquet-Datei als YAML für `sources.yml` |
| `get_parquet_data` | `macros/get_parquet_data.sql` | Beispieldaten einer Parquet-Datei |

### Security

| Macro | Datei | Beschreibung |
|-------|-------|--------------|
| `tenant_key` / `sec_value_key` | `macros/security/tenant_key.sql` | Mandantenschlüssel pro Target / Ausdruck für `dss_sec_value_key` |
| `rls_filter` | `macros/security/rls_filter.sql` | RLS-Prädikat für `_v`-Views |
| `cls_mask` | `macros/security/cls_mask.sql` | Spalten-Maskierung in Views |
| `drop_security_policy` / `apply_security_policy` | `macros/security/security_policy.sql` | Hook-Paar für Security Policies auf physischen Tabellen |
| `grant_select_on_views` | `macros/security/grant_select_on_views.sql` | OLS-Grants auf `mart*`-Views (`on-run-end`) |

> Mandanten- bzw. quellsystemspezifische Macros (z. B. Batch-Loader oder Zeitstempel-Parser für
> eine einzelne Quelle) liegen ebenfalls in `macros/` und sind in der jeweiligen
> Quellsystem-Dokumentation beschrieben.

---

◀ [Changelog](11-changelog.md) · [Übersicht](../README.md) · [Reproduzierbarkeit](13-reproduzierbarkeit.md) ▶
