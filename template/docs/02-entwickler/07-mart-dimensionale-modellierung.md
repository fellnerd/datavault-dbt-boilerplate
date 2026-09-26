---
title: "Mart — Dimensionale Modellierung"
tags:
  - entwickler
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Developer Guide](README.md)

# 📊 Mart — Dimensionale Modellierung

### Überblick

Der Mart Layer implementiert **Star Schema** (Kimball) auf dem Raw Vault.
Dimensionen und Faktentabellen verwenden deterministische BIGINT Surrogate Keys.

**Datenfluss:**
```
Hub/Sat/Link (vault.*) → Current View (sat_*_current_v) → Dimension/Fakt (mart_<domain>.*)
                                                        → publizierte _v-View (RLS/CLS)
```

**Hausmuster:** Die Logik liegt in einer physischen Tabelle (`dim_*`, `fakt_*`), davor steht
eine dünne Wrapper-View (`dim_*_v`, `fakt_*_v`), die publiziert wird und die Security-Macros
trägt. Grund: nicht materialisierte View-Ketten werden bei jedem DirectQuery-Aufruf neu
berechnet und sind bei Ketten bis zu einer External Table zusätzlich instabil
(siehe [Lessons Learned](../lessons-learned/02-dbt-modellierung-materialisierung.md)).

### Surrogate Key Macro

Alle Dimension Keys verwenden das `surrogate_key()` Macro (`macros/surrogate_key.sql`):

```sql
{{ surrogate_key('business_key_column') }} AS person_key
-- Generiert: ABS(CONVERT(BIGINT, HASHBYTES('MD5', CAST(column AS NVARCHAR(MAX)))))
```

- **Typ:** BIGINT (8 Byte, deterministisch, view-kompatibel, Power BI freundlich)
- **Verwendung:** Dimension PK und Fakt FK (gleicher Aufruf für Join-Kompatibilität)

### Dimension Pflicht-Spalten

| Spalte | Typ | Beschreibung | Fallback |
|--------|-----|-------------|----------|
| `{dim}_key` | BIGINT | Surrogate Key via `surrogate_key()` | — |
| `{dim}_id` | NVARCHAR(255) | Technische ID aus Quellsystem | — |
| `{dim}_code` | NVARCHAR(255) | Sprechender Business-Schlüssel | = ID |
| `{dim}_name` | NVARCHAR(255) | Bekannte Bezeichnung | = CODE oder 'UNKNOWN' |
| `dss_load_date` | DATETIME2 | Ladezeitpunkt | — |
| `dss_record_source` | NVARCHAR(255) | Quellenidentifikation | — |

### Beispiel: Dimension

📄 **Datei:** `models/mart/project/dim_person.sql`

```sql
{{ config(materialized='view', tags=['dimension']) }}

SELECT
    {{ surrogate_key('lohnnr') }}                        AS person_key,
    CAST(lohnnr AS NVARCHAR(255))                        AS person_id,
    ISNULL(nachname + ' ' + vorname, 
           CAST(lohnnr AS NVARCHAR(255)))                AS person_code,
    ISNULL(nachname + ' ' + vorname, 'UNKNOWN')          AS person_name,
    sat.dss_load_date,
    sat.dss_record_source
FROM {{ ref('hub_person') }} hub
INNER JOIN {{ ref('sat_person__<quelle>') }} sat
    ON hub.hk_person = sat.hk_person
    AND sat.dss_is_current = 'Y'
```

### Beispiel: Faktentabelle

📄 **Datei:** `models/mart/project/fakt_stunden.sql`

```sql
{{ config(materialized='view', tags=['fact']) }}

SELECT
    {{ surrogate_key('hp.projnr') }}      AS projekt_key,
    {{ surrogate_key('hpsk.code') }}       AS leistungsart_key,
    CONVERT(INT, FORMAT(sat.datum, 'yyyyMMdd')) AS datum_key,
    sat.azbetint                            AS stunden,
    sat.dss_load_date,
    sat.dss_record_source
FROM {{ ref('hub_stundenbuchung') }} h
INNER JOIN {{ ref('sat_stundenbuchung') }} sat
    ON h.hk_stundenbuchung = sat.hk_stundenbuchung
    AND sat.dss_is_current = 'Y'
-- ... weitere Joins zu Hubs für FK-Auflösung
```

### Naming

| Objekt | Pattern | Beispiel |
|--------|---------|---------|
| Dimension | `dim_{entity}` | `dim_person`, `dim_projekt` |
| Faktentabelle | `fakt_{content}` | `fakt_stunden` |
| Publizierte View | `{objekt}_v` | `dim_person_v`, `fakt_stunden_v` |
| Schema (domain) | `mart_{domain}` | `mart_project` |

### Materialisierung
- `materialized='table'` (+ `as_columnstore=false`) — Standard für `dim_*` und `fakt_*`;
  so ist es in `dbt_project.yml` für den Mart-Layer voreingestellt
- `materialized='view'` — für die publizierte `_v`-Wrapper-View und für triviale Objekte
  ohne nennenswerte Joins/Berechnungen
- Security (`rls_filter`, `cls_mask`) gehört in die `_v`-View bzw. — bei physischen
  Fakt-Tabellen — in die Security Policy, siehe [Security in Mart-Models](10-security-in-mart-models-rls-cls.md)

### Schema YAML

Jedes Mart-Modell muss in `_<concept>__models.yml` dokumentiert sein:

```yaml
models:
  - name: dim_person
    description: "Dimension: Mitarbeiterstamm"
    config:
      tags: ['dimension']
    columns:
      - name: person_key
        data_type: bigint
        tests: [not_null, unique]
      - name: person_code
        tests: [not_null]
      - name: person_name
        tests: [not_null]
```

### ER-Diagramm

Pro Mart-Domain: `design/mart/er-mart-<concept>.mmd`

---

◀ [Einzelne Objekte erstellen](06-einzelne-objekte-erstellen.md) · [Übersicht](README.md) · [Mart View erstellen (Legacy Pattern)](08-mart-view-erstellen-legacy-pattern.md) ▶
