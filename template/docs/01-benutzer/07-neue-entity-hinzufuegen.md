---
title: "Neue Entity hinzufügen"
tags:
  - benutzer
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 4. Neue Entity hinzufügen

> Kurzfassung für den Überblick. Der vollständige Weg inklusive Analyse, Namenskonventionen,
> Tests und YAML-Dokumentation steht im
> [Entwicklerhandbuch](../02-entwickler/05-neue-entity-erstellen-komplett.md).
>
> Die folgenden Vorlagen zeigen das Muster an einem Beispielquellsystem.

### Schritt 1: External Table definieren

Bearbeite `models/staging/sources.yml`:

```yaml
- name: ext_neue_entity
  external:
    location: "jira/postgres/public.wp_neue_entity.parquet"
    file_format: ParquetFormat
  columns:
    - name: id
      data_type: BIGINT
    - name: name
      data_type: NVARCHAR(255)
    # ... weitere Spalten
```

### Schritt 2: Staging View erstellen

Erstelle `models/staging/jira_neue_entity.sql`:

```sql
{{- config(
    materialized='view'
) -}}

{%- set yaml_metadata -%}
source_model:
    jira_data: 'ext_neue_entity'
derived_columns:
    dss_record_source: "!jira.wp_neue_entity"
    dss_load_date: "GETDATE()"
hashed_columns:
    hk_neue_entity: 'id'
    hd_neue_entity:
        is_hashdiff: true
        columns:
            - name
            - description
{%- endset -%}

{% set metadata = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(
    include_source_columns=true,
    source_model=metadata['source_model'],
    derived_columns=metadata['derived_columns'],
    hashed_columns=metadata['hashed_columns']
) }}
```

### Schritt 3: Hub erstellen

Erstelle `models/raw_vault/hubs/hub_neue_entity.sql`:

```sql
{{- config(
    materialized='incremental',
    incremental_strategy='append',
    as_columnstore=false
) -}}

{%- set source_model = "jira_neue_entity" -%}
{%- set src_pk = "hk_neue_entity" -%}
{%- set src_nk = "id" -%}
{%- set src_ldts = "dss_load_date" -%}
{%- set src_source = "dss_record_source" -%}

{{ automate_dv.hub(
    src_pk=src_pk, 
    src_nk=src_nk, 
    src_ldts=src_ldts, 
    src_source=src_source, 
    source_model=source_model
) }}
```

### Schritt 4: Satellite erstellen

Erstelle `models/raw_vault/satellites/sat_neue_entity.sql`:

```sql
{{- config(
    materialized='incremental',
    incremental_strategy='append',
    as_columnstore=false
) -}}

{%- set source_model = "jira_neue_entity" -%}
{%- set src_pk = "hk_neue_entity" -%}
{%- set src_hashdiff = "hd_neue_entity" -%}
{%- set src_ldts = "dss_load_date" -%}
{%- set src_source = "dss_record_source" -%}
{%- set src_payload = ["name", "description"] -%}

{{ automate_dv.sat(
    src_pk=src_pk, 
    src_hashdiff=src_hashdiff,
    src_payload=src_payload,
    src_ldts=src_ldts, 
    src_source=src_source, 
    source_model=source_model
) }}
```

### Schritt 5: Deployment

```bash
# External Table erstellen (Development)
dbt run-operation stage_external_sources

# Models bauen (Development)
dbt run --select <concept>_neue_entity hub_neue_entity sat_neue_entity

# Andere Umgebung (Test/Produktion in der Regel über die Pipeline)
dbt run-operation stage_external_sources --target <mandant>-test
dbt run --select <concept>_neue_entity hub_neue_entity sat_neue_entity --target <mandant>-test
```

---

◀ [Verfügbare Targets](06-verfuegbare-targets.md) · [Übersicht](README.md) · [Useful dbt Commands](08-useful-dbt-commands.md) ▶
