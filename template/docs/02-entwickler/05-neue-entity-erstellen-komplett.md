---
title: "Neue Entity erstellen (Komplett)"
tags:
  - entwickler
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Developer Guide](README.md)

# 🏗️ Neue Entity erstellen (Komplett)

### Szenario
Eine komplett neue Entity soll ins Data Vault (z.B. `product` aus einer neuen Quelltabelle).

### Übersicht der Schritte

```
┌──────────────────────────────────────────────────────────────────┐
│  1. External Table    →  2. Staging View  →  3. Hub             │
│        ↓                                          ↓              │
│  sources.yml               jira_product.sql      hub_product.sql │
│                                   ↓                    ↓         │
│                            4. Satellite         5. Link          │
│                            sat_product.sql      link_*.sql       │
│                                   ↓                              │
│                            6. Tests & Deploy                     │
└──────────────────────────────────────────────────────────────────┘
```

### Schritt 1: External Table definieren

📄 **Datei:** [models/staging/sources.yml](../../models/staging/sources.yml)

```yaml
sources:
  - name: staging
    database: "{{ target.database }}"
    schema: stg
    tables:
      # ... bestehende Tabellen ...
      
      # ═══════════════════════════════════════════
      # NEU: Product
      # ═══════════════════════════════════════════
      - name: ext_jira_product
        external:
          location: "jira/postgres/public.wp_product.parquet"
          file_format: ParquetFormat
        columns:
          - name: object_id
            data_type: BIGINT
            tests:
              - not_null
          - name: name
            data_type: NVARCHAR(255)
          - name: description
            data_type: NVARCHAR(MAX)
          - name: price
            data_type: DECIMAL(18,2)
          - name: category_id
            data_type: BIGINT
          - name: dss_record_source
            data_type: NVARCHAR(100)
          - name: dss_load_date
            data_type: DATETIME2
          - name: dss_run_id
            data_type: NVARCHAR(100)
```

### Schritt 2: Staging View erstellen

📄 **Neue Datei:** `models/staging/jira_product.sql`

Staging Views verwenden das **automate_dv.stage() YAML Metadata Pattern**. Alle Hash Keys und Hash Diffs werden automatisch von automate_dv berechnet (mit Custom Overrides in `macros/hash_override.sql`).

```sql
/*
 * Staging Model: jira_product
 *
 * Source: ext_jira_product (Product-Daten)
 * Business Key: object_id
 * Hash Key: hk_product
 * Payload: 4 Spalten — Product-Attribute
 *
 * Uses automate_dv.stage() macro for standardized staging.
 */

{%- set yaml_metadata -%}
source_model:
  staging: "ext_jira_product"

derived_columns:
  dss_record_source: "!jira"
  dss_load_date: "COALESCE(TRY_CAST(dss_load_date AS DATETIME2), GETDATE())"
  dss_create_datetime: "GETDATE()"
  dss_business_key: "CONCAT_WS('||', 'default', 'default', ISNULL(LTRIM(RTRIM(CAST(object_id AS NVARCHAR(MAX)))), '-1'))"

hashed_columns:
  hk_product: "object_id"
  hk_category: "category_id"
  hk_link_product_category:
    - "object_id"
    - "category_id"
  hd_product:
    is_hashdiff: true
    columns:
      - "category_id"
      - "description"
      - "name"
      - "price"
{%- endset -%}

{% set metadata_dict = fromyaml(yaml_metadata) %}

{{ automate_dv.stage(include_source_columns=true,
                     source_model=metadata_dict['source_model'],
                     derived_columns=metadata_dict['derived_columns'],
                     hashed_columns=metadata_dict['hashed_columns']) }}
```

> **Referenz-Beispiele im Repository:**
> - Single BK + Reserved Keyword: `models/staging/<mandant>_lohn_len_main.sql`
> - Composite BK: `models/staging/<mandant>_proj_nsa_main.sql`
> - Multiple Reserved Keywords: `models/staging/<mandant>_fibu_fhe_main.sql`

### Schritt 3: Hub erstellen

📄 **Neue Datei:** `models/raw_vault/hubs/hub_product.sql`

```sql
/*
 * Hub: hub_product
 * Schema: vault
 * 
 * Speichert eindeutige Product Business Keys.
 * Insert-Only: Neue Products werden hinzugefügt, nie gelöscht.
 */

{{ config(
    materialized='incremental',
    unique_key='hk_product',
    as_columnstore=false
) }}

WITH source_data AS (
    SELECT DISTINCT
        hk_product,
        object_id,
        dss_load_date,
        dss_record_source
    FROM {{ ref('jira_product') }}
    WHERE hk_product IS NOT NULL
),

{% if is_incremental() %}
existing_hubs AS (
    SELECT hk_product FROM {{ this }}
),
{% endif %}

new_records AS (
    SELECT
        src.hk_product,
        src.object_id,
        src.dss_load_date,
        src.dss_record_source
    FROM source_data src
    {% if is_incremental() %}
    WHERE NOT EXISTS (
        SELECT 1 FROM existing_hubs eh
        WHERE eh.hk_product = src.hk_product
    )
    {% endif %}
)

SELECT * FROM new_records
```

### Schritt 4: Satellite erstellen

📄 **Neue Datei:** `models/raw_vault/satellites/sat_product.sql`

```sql
/*
 * Satellite: sat_product
 * Schema: vault
 * 
 * Speichert Product-Attribute mit vollständiger Historie.
 * dss_is_current: 'Y' für aktuellen Eintrag
 * dss_end_date: Ende der Gültigkeit
 */

{{ config(
    materialized='incremental',
    unique_key='hk_product',
    as_columnstore=false,
    post_hook=[
        "{{ update_satellite_current_flag(this, 'hk_product') }}"
    ]
) }}

WITH source_data AS (
    SELECT 
        hk_product,
        hd_product,
        dss_load_date,
        dss_record_source,
        -- Payload
        name,
        description,
        price,
        category_id
    FROM {{ ref('jira_product') }}
    WHERE hk_product IS NOT NULL
),

{% if is_incremental() %}
existing_sats AS (
    SELECT 
        hk_product,
        hd_product
    FROM {{ this }}
),
{% endif %}

new_records AS (
    SELECT
        src.hk_product,
        src.hd_product,
        src.dss_load_date,
        src.dss_record_source,
        src.name,
        src.description,
        src.price,
        src.category_id
    FROM source_data src
    {% if is_incremental() %}
    WHERE NOT EXISTS (
        SELECT 1 FROM existing_sats es
        WHERE es.hk_product = src.hk_product
          AND es.hd_product = src.hd_product
    )
    {% endif %}
)

SELECT 
    *,
    'Y' AS dss_is_current,
    CAST(NULL AS DATETIME2) AS dss_end_date
FROM new_records
```

### Schritt 5: Schema YAML erstellen (WICHTIG!)

⚠️ **Jedes Model MUSS in einer Schema YAML-Datei dokumentiert werden!**

Die VS Code Extension und dbt-Dokumentation verwenden diese Dateien für Spalten-Metadaten.

#### Datei-Namenskonvention

| Layer | Datei | Speicherort |
|-------|------|-------------|
| Staging | `_staging__models.yml` | `models/staging/` |
| Raw Vault | `_<concept>__models.yml` | `models/raw_vault/<concept>/` |
| Business Vault | `_business_vault__models.yml` | `models/business_vault/` |
| Mart | `_<concept>__models.yml` | `models/mart/<concept>/` |

#### Vorlage

📄 **Datei:** `models/raw_vault/<concept>/_<concept>__models.yml`

```yaml
version: 2

models:
  # ═══════════════════════════════════════════
  # Staging: Product
  # ═══════════════════════════════════════════
  - name: <concept>_product
    description: Staging view for product with hash calculations
    columns:
      - name: hk_product
        description: Hash Key (Primary Key)
        data_type: char(64)
        tests:
          - not_null
      - name: object_id
        description: Business Key from source
        data_type: bigint
        tests:
          - not_null
      - name: name
        description: Product name
        data_type: nvarchar(4000)
      - name: dss_load_date
        description: Load timestamp
        data_type: datetime2(7)
        tests:
          - not_null
      - name: dss_record_source
        description: Data source identifier
        data_type: varchar(100)
        tests:
          - not_null

  # ═══════════════════════════════════════════
  # Hub: Product
  # ═══════════════════════════════════════════
  - name: hub_product
    description: Hub containing unique product business keys
    columns:
      - name: hk_product
        description: Hash Key (Primary Key)
        data_type: char(64)
        tests:
          - unique
          - not_null
      - name: object_id
        description: Business Key
        data_type: bigint
        tests:
          - not_null
      - name: dss_load_date
        description: First load timestamp
        data_type: datetime2(7)
        tests:
          - not_null
      - name: dss_record_source
        description: Data source
        data_type: varchar(100)
        tests:
          - not_null

  # ═══════════════════════════════════════════
  # Satellite: Product
  # ═══════════════════════════════════════════
  - name: sat_product
    description: Satellite with product descriptive attributes
    columns:
      - name: hk_product
        description: Hash Key (Foreign Key to Hub)
        data_type: char(64)
        tests:
          - not_null
          - relationships:
              to: ref('hub_product')
              field: hk_product
      - name: hd_product
        description: Hash Diff for change detection
        data_type: char(64)
        tests:
          - not_null
      - name: name
        description: Product name
        data_type: nvarchar(4000)
      - name: dss_load_date
        description: Load timestamp
        data_type: datetime2(7)
      - name: dss_record_source
        description: Data source
        data_type: varchar(100)
```

#### Spalten aus Datenbank generieren

Spaltendefinitionen lassen sich aus bestehenden Views ableiten:

```sql
SELECT c.name, t.name AS data_type, c.max_length, c.precision, c.scale, c.is_nullable
FROM sys.views v
JOIN sys.columns c ON v.object_id = c.object_id
JOIN sys.types t ON c.user_type_id = t.user_type_id
WHERE SCHEMA_NAME(v.schema_id) = 'stg' AND v.name = '<view_name>'
ORDER BY c.column_id;
```

### Schritt 6: Deployment

```bash
# 1. External Table erstellen
dbt run-operation stage_external_sources
# oder einzelne Tabelle
dbt run-operation stage_external_sources --args 'select: staging.ext_jira_product'

# 2. Alle neuen Models bauen (mit Upstream-Dependencies)
dbt run --select +raw_vault.<concept>.hub_product +raw_vault.<concept>.sat_product

# 3. Tests ausführen
dbt test --select raw_vault.<concept>.hub_product raw_vault.<concept>.sat_product

# 4. Ghost Records hinzufügen (optional)
# → Macro in ghost_records.sql erweitern
```

---

◀ [Neues Attribut hinzufügen](04-neues-attribut-hinzufuegen.md) · [Übersicht](README.md) · [Einzelne Objekte erstellen](06-einzelne-objekte-erstellen.md) ▶
