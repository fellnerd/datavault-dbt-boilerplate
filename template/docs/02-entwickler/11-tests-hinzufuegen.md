---
title: "Tests hinzufügen"
tags:
  - entwickler
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Developer Guide](README.md)

# 🧪 Tests hinzufügen

### Test-Typen

| Test | Zweck | Beispiel |
|------|-------|----------|
| `not_null` | Spalte darf nicht NULL sein | Primary Keys, Business Keys |
| `unique` | Werte müssen eindeutig sein | Hash Keys in Hubs |
| `relationships` | FK-Beziehung validieren | Satellite → Hub |
| `accepted_values` | Nur bestimmte Werte erlaubt | Status-Felder |

### Tests in schema.yml

📄 **Datei:** [models/schema.yml](../../models/schema.yml)

```yaml
models:
  - name: hub_<entity>
    columns:
      - name: hk_<entity>
        tests:
          - unique
          - not_null
      - name: <business_key>
        tests:
          - not_null

  - name: sat_<entity>
    columns:
      - name: hk_<entity>
        tests:
          - not_null
          - relationships:
              to: ref('hub_<entity>')
              field: hk_<entity>
      - name: hd_<entity>
        tests:
          - not_null
      - name: dss_is_current
        tests:
          - accepted_values:
              values: ['Y', 'N']
```

### Tests ausführen

```bash
# Alle Tests
dbt test

# Tests für bestimmtes Model
dbt test --select hub_company

# Tests für Tag
dbt test --select tag:hub
```

---

◀ [Security in Mart-Models (RLS/CLS)](10-security-in-mart-models-rls-cls.md) · [Übersicht](README.md) · [Deployment Workflow](12-deployment-workflow.md) ▶
