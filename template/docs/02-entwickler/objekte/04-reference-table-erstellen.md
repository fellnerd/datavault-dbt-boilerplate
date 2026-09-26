---
title: "Reference Table erstellen"
tags:
  - entwickler/vault-objekte
---
[Dokumentation](../../README.md) › [Data Vault 2.1 - Developer Guide](../README.md) › [Einzelne Objekte erstellen](README.md)

# 5.4 Reference Table erstellen

📄 **Beispiele im Repository:** [seeds/](../../../seeds) (Reference Data als CSV) und `models/raw_vault/_common/refs`

**Schritt 1:** CSV-Datei erstellen

```csv
role_code,role_name,role_description
CLIENT,Kunde,Unternehmen das Dienstleistungen bezieht
CONTRACTOR,Auftragnehmer,Unternehmen das Aufträge ausführt
SUPPLIER,Lieferant,Unternehmen das Waren liefert
```

📄 **Speichern als:** `seeds/ref_<name>.csv`

**Schritt 2:** Konfiguration in dbt_project.yml

📄 **Datei:** [dbt_project.yml](../../../dbt_project.yml)

```yaml
seeds:
  datavault:
    +schema: vault
    ref_<name>:
      +column_types:
        <column>: VARCHAR(50)
```

**Schritt 3:** Deployment

```bash
dbt seed --select ref_<name>
```

---

◀ [Link erstellen](03-link-erstellen.md) · [Einzelne Objekte erstellen](README.md) · [PSA (Persistent Staging Area) erstellen](05-psa-persistent-staging-area-erstellen.md) ▶
