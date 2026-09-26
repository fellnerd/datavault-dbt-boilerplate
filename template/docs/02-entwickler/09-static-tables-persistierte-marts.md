---
title: "Static Tables (Persistierte Marts)"
tags:
  - entwickler
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Developer Guide](README.md)

# 📦 Static Tables (Persistierte Marts)

> **Stand:** Dieses Muster ist im aktuellen Projekt **nicht konfiguriert** — es gibt weder ein
> Schema `mart_static` noch einen Ordner `models/mart/tables/` oder den Tag `static`.
> Mart-Objekte werden heute standardmässig als Tabelle mit `_v`-Wrapper-View gebaut
> (siehe [Mart — Dimensionale Modellierung](07-mart-dimensionale-modellierung.md)).
> Das Kapitel bleibt als Vorlage für den Fall, dass eine eigene persistierte Schicht mit
> MERGE-Strategie benötigt wird; Schema, Ordner und Tag müssten dann in `dbt_project.yml`
> ergänzt werden. Die Index-Macros im unteren Teil sind dagegen aktuell und im Einsatz.

### Übersicht

Static Tables sind persistierte Tabellen im Mart-Layer mit folgenden Eigenschaften:

| Eigenschaft | Beschreibung |
|-------------|--------------|
| **Schema** | `mart_static` |
| **Materialisierung** | `incremental` mit MERGE-Strategie |
| **Index** | Non-Clustered auf Hash Key |
| **Change Detection** | via `last_updated` (MAX aus Satellite Load Dates) |
| **Tag** | `static` für Batch-Updates |

### Wann Static Table vs. View?

| Kriterium | View | Static Table |
|-----------|------|--------------|
| Daten-Aktualität | Real-time | Refresh bei `dbt run` |
| Komplexität | 1-2 JOINs | Viele JOINs |
| Abfrage-Häufigkeit | Selten | Häufig (BI-Dashboards) |
| Performance | Gut | Sehr gut (Index) |
| Speicher | Kein | Tabelle + Index |

### Static Table erstellen

📄 **Neue Datei:** `models/mart/tables/<name>.sql`

**Beispiel: Aktuelle Firmendaten (persistiert)**

```sql
/*
 * Static Table: company_current
 * Schema: mart_static
 * 
 * Persistierte Tabelle mit aktuellen Firmendaten.
 * Inkrementelle Updates via MERGE auf hk_company.
 */

{{ config(
    materialized='incremental',
    unique_key='hk_company',
    incremental_strategy='merge',
    merge_update_columns=['name', 'city', 'street', 'last_updated'],
    as_columnstore=false,
    tags=['static'],
    post_hook=[
        "{{ create_hash_index('hk_company') }}"
    ]
) }}

WITH source_data AS (
    SELECT
        -- Hash Key
        h.hk_company,
        h.object_id,
        
        -- Payload
        s.name,
        s.city,
        s.street,
        
        -- Metadata
        h.dss_load_date AS hub_load_date,
        s.dss_load_date AS last_updated

    FROM {{ ref('hub_company') }} h

    -- Aktuelle Satellite-Daten
    LEFT JOIN {{ ref('sat_company') }} s
        ON h.hk_company = s.hk_company
        AND s.dss_is_current = 'Y'

    -- Ghost Records ausschließen
    WHERE h.object_id > 0
)

SELECT * FROM source_data
{% if is_incremental() %}
WHERE last_updated > (SELECT MAX(last_updated) FROM {{ this }})
{% endif %}
```

### Index Macros

Die folgenden Macros stehen für Index-Erstellung zur Verfügung:

| Macro | Beschreibung |
|-------|--------------|
| `create_hash_index(column)` | Non-Clustered Index auf einer Spalte |
| `create_composite_index([col1, col2])` | Index auf mehreren Spalten |
| `drop_and_create_index(column)` | Index neu erstellen (bei Schema-Änderungen) |

**Verwendung als post_hook:**

```sql
{{ config(
    post_hook=[
        "{{ create_hash_index('hk_company') }}",
        "{{ create_composite_index(['hk_company', 'hk_project']) }}"
    ]
) }}
```

### Deployment

```bash
# Initial Load (Full Refresh) - ERSTE AUSFÜHRUNG
dbt run --select company_current --full-refresh

# Inkrementelles Update
dbt run --select company_current

# Alle Static Tables aktualisieren
dbt run --select tag:static

# Full Refresh für alle Static Tables (z.B. wöchentlich)
dbt run --select tag:static --full-refresh
```

### Index verifizieren

```sql
-- Index prüfen
SELECT 
    i.name AS index_name,
    i.type_desc,
    c.name AS column_name
FROM sys.indexes i
JOIN sys.index_columns ic ON i.object_id = ic.object_id AND i.index_id = ic.index_id
JOIN sys.columns c ON ic.object_id = c.object_id AND ic.column_id = c.column_id
WHERE i.object_id = OBJECT_ID('mart_static.company_current')
```

### CLI Command

```bash
dbt run --select mart_static.company_current
```

---

◀ [Mart View erstellen (Legacy Pattern)](08-mart-view-erstellen-legacy-pattern.md) · [Übersicht](README.md) · [Security in Mart-Models (RLS/CLS)](10-security-in-mart-models-rls-cls.md) ▶
