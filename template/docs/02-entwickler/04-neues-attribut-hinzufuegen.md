---
title: "Neues Attribut hinzufügen"
tags:
  - entwickler
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Developer Guide](README.md)

# ➕ Neues Attribut hinzufügen

### Szenario
Ein bestehendes Attribut soll zum Satellite hinzugefügt werden (z.B. `tax_number` zu `sat_company`).

### Schritt-für-Schritt

#### Schritt 1: External Table erweitern

📄 **Datei:** [models/staging/sources.yml](../../models/staging/sources.yml)

```yaml
# Finde die External Table und füge die Spalte hinzu
- name: ext_jira_company
  columns:
    # ... bestehende Spalten ...
    - name: tax_number          # ← NEU
      data_type: NVARCHAR(50)   # ← Datentyp
```

#### Schritt 2: Staging View erweitern

📄 **Datei:** `models/staging/<concept>_<entity>.sql`

Staging Views verwenden das automate_dv.stage() YAML Metadata Pattern. Füge die neue Spalte zum `hashed_columns` Block hinzu:

```yaml
# In der yaml_metadata Sektion:
hashed_columns:
  hk_company: "object_id"
  hd_company:
    is_hashdiff: true
    columns:
      - "name"
      - "street"
      # ... bestehende ...
      - "tax_number"               # ← NEU (falls Änderungen getrackt werden sollen)
```

> **Hinweis:** Hashdiff-Spalten werden automatisch alphabetisch sortiert durch automate_dv. Die Spalte muss an der richtigen alphabetischen Position eingefügt werden.

#### Schritt 3: Satellite erweitern

📄 **Datei:** `models/raw_vault/<_common|concept>/satellites/sat_<entity>__<quelle>.sql`

```sql
WITH source_data AS (
    SELECT 
        hk_company,
        hd_company,
        -- ... bestehende Spalten ...
        tax_number,              -- ← NEU
        dss_load_date,
        dss_record_source
    FROM {{ ref('jira_company') }}
    WHERE hk_company IS NOT NULL
),
-- ... Rest bleibt gleich ...
```

#### Schritt 4: Deployment

```bash
# External Table aktualisieren
dbt run-operation stage_external_sources

# Satellite neu bauen (full-refresh wegen Schemaänderung!)
dbt run --full-refresh --select jira_company sat_company

# Tests ausführen
dbt test --select sat_company
```

### ⚠️ Wichtig
- Bei **Schema-Änderungen** immer `--full-refresh` verwenden
- Hash Diff nur erweitern wenn Änderungen getrackt werden sollen
- Nach Änderung: Tests ausführen!

---

◀ [Projektstruktur](03-projektstruktur.md) · [Übersicht](README.md) · [Neue Entity erstellen (Komplett)](05-neue-entity-erstellen-komplett.md) ▶
