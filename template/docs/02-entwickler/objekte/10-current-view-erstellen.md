---
title: "Current View erstellen (sat_*_current_v)"
tags:
  - entwickler/vault-objekte
---
[Dokumentation](../../README.md) › [Data Vault 2.1 - Developer Guide](../README.md) › [Einzelne Objekte erstellen](README.md)

# 5.10 Current View erstellen (sat_*_current_v)

Für jeden Satellite wird eine Current View erstellt, die den aktuellen Stand bereitstellt. Mart-Modelle referenzieren diese Views statt der Satellites direkt.

📄 **Datei:** `models/raw_vault/_common/satellites/sat_<entity>_current_v.sql`

```sql
{{ config(materialized='view') }}
{{ satellite_current_view(
    satellite_model='sat_<entity>',
    hashkey_column='hk_<entity>'
) }}
```

**Zugriffsmuster:**
- **SCD1 (aktueller Stand):** `WHERE dss_is_current = 'Y'`
- **SCD2 (volle Historie):** Kein Filter, alle Records

**Datenfluss:**
```
Hub/Sat (vault.*) → Current View (sat_*_current_v) → Mart (mart_*.*)
```

---

◀ [PIT Table erstellen](09-pit-table-erstellen.md) · [Einzelne Objekte erstellen](README.md)
