---
title: "Best Practices"
tags:
  - benutzer
---
[Dokumentation](../README.md) › [Data Vault 2.1 - Benutzer-Dokumentation](README.md)

# 8. Best Practices

### 8.1 Development Workflow

1. **Entwickeln** gegen das Development-Target
2. **Testen** mit `dbt test`
3. **Review** der generierten SQL in `target/compiled/`
4. **Commit** und Merge Request — die CI validiert Kompilierung und Tests
5. **Deploy** nach Test und Produktion über die Pipeline (siehe [CI/CD](../03-system/allgemein/10-ci-cd-pipeline.md))

### 8.2 Naming Conventions

| Objekt | Pattern | Beispiel |
|--------|---------|----------|
| External Table | `ext_<concept>_<entity>` | `ext_crm_kunde` |
| Staging View | `<concept>_<entity>` | `crm_kunde` |
| Hub | `hub_<entity>` | `hub_kunde` |
| Satellite | `sat_<entity>__<quelle>` | `sat_kunde__crm` |
| Link | `link_<e1>_<e2>` | `link_kunde_vertrag` |
| Hash Key | `hk_<entity>` | `hk_kunde` |
| Hash Diff | `hd_<entity>__<quelle>` | `hd_kunde__crm` |

### 8.3 Änderungen nachvollziehen

```bash
# Letzte Änderungen
git log --oneline -10

# Diff zu letztem Commit
git diff

# Model-History in Vault
SELECT * FROM vault.sat_<entity>__<quelle>
WHERE hk_<entity> = '<hash>'
ORDER BY dss_load_date DESC;
```

---

◀ [Daten prüfen](10-daten-pruefen.md) · [Übersicht](README.md) · [Datenzugriff & Berechtigungen (Security)](12-datenzugriff-berechtigungen-security.md) ▶
