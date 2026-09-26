---
title: "Mart View erstellen (Legacy Pattern)"
tags:
  - entwickler
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Developer Guide](README.md)

# 📊 Mart View erstellen (Legacy Pattern)

> **Hinweis:** Dieses Pattern wird durch das obige Star Schema Pattern abgelöst.
> Für neue Mart-Objekte verwende Dimensionen und Faktentabellen mit `surrogate_key()`.

### Szenario
Eine flache View für BI-Tools (Power BI, Excel) erstellen.

📄 **Neue Datei:** `models/mart/v_<name>.sql`

**Beispiel: Aktuelle Firmendaten**

```sql
/*
 * Mart View: v_company_current
 * Schema: mart_project
 * 
 * Flache View mit aktuellen Firmendaten für Reporting.
 */

{{ config(
    materialized='view'
) }}

SELECT
    -- IDs (für Joins)
    h.hk_company,
    h.object_id,
    h.source_table,
    
    -- Stammdaten
    s.name AS company_name,
    s.street,
    s.citycode AS zip_code,
    s.city,
    s.country AS country_id,
    co.name AS country_name,
    
    -- Kontakt
    s.email,
    s.phone,
    s.mobile,
    s.website,
    
    -- Finanzen
    s.iban,
    s.bic,
    s.credit_rating,
    
    -- Rolle
    lr.role_code,
    r.role_name,
    
    -- Metadata
    s.dss_load_date AS last_updated,
    s.dss_record_source AS source_system

FROM {{ ref('hub_company') }} h

-- Aktuelle Satellite-Daten
INNER JOIN {{ ref('sat_company') }} s 
    ON h.hk_company = s.hk_company 
    AND s.dss_is_current = 'Y'

-- Rolle
LEFT JOIN {{ ref('link_company_role') }} lr 
    ON h.hk_company = lr.hk_company
LEFT JOIN {{ ref('ref_role') }} r 
    ON lr.role_code = r.role_code

-- Land
LEFT JOIN {{ ref('link_company_country') }} lc 
    ON h.hk_company = lc.hk_company
LEFT JOIN {{ ref('sat_country') }} co 
    ON lc.hk_country = co.hk_country 
    AND co.dss_is_current = 'Y'

-- Ghost Records ausschließen
WHERE h.object_id > 0
```

**Konfiguration in dbt_project.yml:**

```yaml
models:
  datavault:
    mart:
      +schema: mart_project
      +materialized: view
```

**Deployment:**

```bash
dbt run --select v_company_current
```

---

◀ [Mart — Dimensionale Modellierung](07-mart-dimensionale-modellierung.md) · [Übersicht](README.md) · [Static Tables (Persistierte Marts)](09-static-tables-persistierte-marts.md) ▶
